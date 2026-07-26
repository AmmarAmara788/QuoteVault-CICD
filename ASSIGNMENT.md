# Assignment — Build the CI/CD pipeline for QuoteVault

You are given a **complete, working, already-Dockerized** application. The app code, the tests,
and the **Dockerfile all work**. The only thing missing is the **CI/CD pipeline**.

**Your job:** write the two GitHub Actions workflows so every change is automatically tested and
every good build is automatically published.

> Do not modify the application code or the Dockerfile. You only write the two workflow files
> (plus your `REPORT.md`).

---

## 1. What you're given (all working)
```
quotevault/            the Flask app  (app.py, validation.py)
wsgi.py                gunicorn entry point
tests/unit/            5 unit tests   (pure logic)
tests/api/             5 API tests    (Flask test client)
requirements.txt       app dependencies
requirements-dev.txt   pytest + flake8
Dockerfile             ✅ WORKING — builds the image
.dockerignore          ✅ WORKING
docker-compose.yml     ✅ WORKING — runs the app locally
```

Prove it all works before you start:
```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest -q                      # 10 tests pass

docker compose up --build      # http://localhost:8000
curl localhost:8000/health     # {"status":"ok"}
```

The API stores quotes **in memory** — there is **no database** to configure.
```
GET  /health                → { "status": "ok" }
GET  /api/quotes           → list quotes
POST /api/quotes           → add    { "text", "author" }
GET  /api/quotes/random    → a random quote (404 if none)
```

---

## 2. What YOU must write (these two files are EMPTY)
```
.github/workflows/ci.yml     ← empty — you write it
.github/workflows/cd.yml     ← empty — you write it
```

### 2.1 `ci.yml` — Continuous Integration
**Triggers:** every `push` **and** `pull_request` targeting `main`.

**Four jobs**, wired with `needs:` in this shape:
```
lint ─┬─ unit-tests ─┐
      └─ api-tests ──┴─ docker-build
```
| Job | Must do |
|-----|---------|
| `lint` | check out code, set up Python 3.12, install `requirements-dev.txt`, run `flake8 quotevault` |
| `unit-tests` | after lint — install deps, run `pytest tests/unit -q` |
| `api-tests` | after lint — install deps, run `pytest tests/api -q` |
| `docker-build` | after **both** test jobs — `docker build` the image, run the container, and **smoke-test** `curl http://localhost:8000/health`; clean up the container even if a step fails |

Requirements:
- Use `actions/checkout` and `actions/setup-python`.
- Use `needs:` so the order above is enforced (don't build a broken app).
- The smoke test must **retry for a few seconds** (the app needs a moment to start) and **fail the
  job** if `/health` never answers.
- The cleanup step must run even on failure (`if: always()`).

### 2.2 `cd.yml` — Continuous Deployment
**Triggers:** `push` to `main`, **and** tags matching `v*.*.*`.

Must:
1. Set **least-privilege** `permissions:` (`contents: read`, `packages: write`).
2. Log in to **GHCR** (`ghcr.io`) using `${{ github.actor }}` and the built-in
   `${{ secrets.GITHUB_TOKEN }}` — **no personal tokens, no hard-coded secrets**.
3. Build the image and **push** it to `ghcr.io/<owner>/<repo>` with these tags:
   - the branch name, the commit `sha`, `latest` (only on the default branch), and the **semver**
     version when a `vX.Y.Z` tag triggers the run.
4. In a **second job**, create a **GitHub Release** — but only when the run was triggered by a
   version tag (use an `if:` condition on `github.ref`).

---

## 3. Definition of done (test it yourself)
- [ ] Push to a **branch** / open a PR → CI runs and **all four jobs pass**; **nothing is published**.
- [ ] Merge to **`main`** → CI passes **and** CD publishes the image; it appears under the repo's
      **Packages**.
- [ ] `docker pull ghcr.io/<owner>/<repo>:latest` then
      `docker run -p 8000:8000 ghcr.io/<owner>/<repo>:latest` → `curl localhost:8000/health` works.
- [ ] `git tag v1.0.0 && git push origin v1.0.0` → a **`1.0.0`** image tag **and** a **GitHub
      Release** are created.
- [ ] Breaking a test on purpose makes CI go **red** and nothing gets published.

---

## 4. Deliverables
```
.github/workflows/ci.yml     your CI pipeline
.github/workflows/cd.yml     your CD pipeline
REPORT.md                    see below
```
**`REPORT.md`** must include:
1. A screenshot (or pasted log) of a **green CI run** showing all four jobs.
2. The **image URL** you published, and the output of `docker pull` + `docker run` + `curl /health`.
3. Proof of a **release**: the tag you pushed and the resulting image tag + Release.
4. One failure you caused on purpose, and how the pipeline reacted.
5. Two sentences: what is the difference between your CI and your CD workflow?

---

## 5. Hints
- Every job runs on a **fresh machine** — each one needs its own `checkout` + `setup-python` +
  install steps.
- `needs: [a, b]` waits for **both**.
- `docker/login-action`, `docker/metadata-action` and `docker/build-push-action` do the heavy
  lifting in CD — read their inputs.
- Image names must be **lowercase**; `ghcr.io/${{ github.repository }}` handles that for you.
- If the CD job fails with `denied: permission_denied`, check your `permissions:` block.
