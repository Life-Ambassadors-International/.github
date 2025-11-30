# TEQUMSA Git Service

Minimal FastAPI service for securely writing `recognition` records into a mounted repository and committing/pushing changes.

## Endpoints (OpenAPI available in openapi.yaml)
- `POST /v1/recognition` — write `recognition`, append to `data/recognition_metrics.json`, git add/commit/push (HMAC-SHA256 required)
- `POST /v1/pull` — fetch & hard reset to origin/BRANCH (HMAC-SHA256 required)
- `GET  /v1/status` — show current HEAD & branch

## Auth
Requests must include header:
`X-TEQ-Signature: sha256=<hex>`
where `<hex>` = HMAC-SHA256(body, TEQ_HMAC_SECRET)

## Deploy
- Mount your repo at `/repo`
- Set `TEQ_HMAC_SECRET` as a strong secret
- Use a deploy key (SSH) or HTTPS access token for git push
- Run with Docker / docker-compose (see docker-compose.yml)
