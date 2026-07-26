# Assignment — Add CI/CD to the QuoteVault API

You are given a **working** Flask "QuoteVault API" (it stores quotes in memory, so it runs with no
database). The application code and tests are complete. **The Docker and CI/CD files are present
but EMPTY** — your job is to fill them in.

**Do not modify the application code.** Only write the Docker/CI/CD files, plus your `REPORT.md`.

## The app
```
GET  /health                 → { "status": "ok" }
GET  /api/quotes            → list quotes
POST /api/quotes            → add    { "text", "author" }
GET  /api/quotes/random     → a random quote (404 if none)
```
Run tests locally:
```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest -q          # 10 tests should pass
```

## Empty files to fill in
```
Dockerfile                       ← empty
.dockerignore                    ← empty
docker-compose.yml               ← empty
.github/workflows/ci.yml         ← empty
.github/workflows/cd.yml         ← empty
```

## What to deliver
1. **`Dockerfile`** — a Python image that installs `requirements.txt`, copies the `quotevault`
   package + `wsgi.py`, runs as a **non-root** user, exposes the port, and starts the app with
   **gunicorn** (`gunicorn -b 0.0.0.0:8000 wsgi:app`). Order steps for layer caching (deps first).
2. **`.dockerignore`** — keep tests, `__pycache__`, `.git`, and the Docker files out of the build
   context.
3. **`docker-compose.yml`** — run the API (published on 8000). No database needed.
4. **`.github/workflows/ci.yml`** — on push/PR to `main`, run **four jobs**: `flake8` lint,
   `pytest tests/unit`, `pytest tests/api`, and a `docker build` + `curl /health` smoke test.
   Use `needs:` so lint runs first and docker-build runs after the tests.
5. **`.github/workflows/cd.yml`** — on push to `main` and on `vX.Y.Z` tags, **build and push** the
   image to **GHCR** (`ghcr.io/<owner>/<repo>`) using the built-in `GITHUB_TOKEN`, with
   least-privilege `permissions`. On a version tag, also create a **GitHub Release**.

## Definition of done
- [ ] `docker compose up --build` runs the API; `curl localhost:8000/health` → `{"status":"ok"}`.
- [ ] Push to a branch → CI runs all four jobs green; **nothing is published**.
- [ ] Merge to `main` → CI + CD run; the image appears under the repo's **Packages** (GHCR).
- [ ] `git tag v1.0.0 && git push origin v1.0.0` → a semver image + a GitHub Release.
- [ ] `docker run -p 8000:8000 ghcr.io/<owner>/<repo>:latest` runs the app standalone.

Grading rubric and hints are in your course handout.
