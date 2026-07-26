# QuoteVault — CI/CD Assignment (student)

A small Flask **QuoteVault API** that is already **fully working and Dockerized**. The app, the
tests and the `Dockerfile` are done.

**Your task: write the CI/CD pipeline.** The two workflow files exist but are **empty**:
```
.github/workflows/ci.yml     ← YOU write (lint → unit → api → docker build + smoke test)
.github/workflows/cd.yml     ← YOU write (build & push image to GHCR, release on tags)
```

Start here → **[`ASSIGNMENT.md`](ASSIGNMENT.md)**

## Check that everything works before you start
```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest -q                      # 10 tests pass

docker compose up --build      # http://localhost:8000
curl localhost:8000/health     # {"status":"ok"}
```

## The API
```
GET  /health               GET  /api/quotes
POST /api/quotes           GET  /api/quotes/random
```
Quotes are stored in memory — no database needed.
