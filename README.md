# PrepareMe

PrepareMe is a curriculum-aware institutional AI learning operating system.

This repository is being built from three source-of-truth documents:

- `PrepareMe_Blueprint.md`
- `PrepareMe_Codex_Prompt.md`
- `PrepareMe_Execution_Playbook.md`

## Repository Layout

- `backend/`: FastAPI monolith, async workers, migrations, tests
- `frontend/`: Next.js App Router client shell
- `docs/`: architecture notes and runbooks
- `infra/`: local deployment assets

## Current Phase

Phase 0 foundation:

- tenant-aware backend substrate
- explicit auth and institution context
- PostgreSQL schema baseline and RLS migration
- LLM, storage, logging, and task orchestration boundaries
- initial frontend shell

## Local Run

### Prerequisites

- Python 3.11+ for local development
- Node 24+
- npm 11+
- Optional but recommended: Docker Desktop for PostgreSQL + Redis

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python -m pip install -e ".[dev]"
copy ..\.env.example .env
.\.venv\Scripts\python -m alembic upgrade head
.\.venv\Scripts\python -m uvicorn app.main:app --reload --port 8000
```

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

### Local Infrastructure

```powershell
cd infra\docker
docker compose -f docker-compose.dev.yml up -d
```

The development Postgres container is exposed on `localhost:5433` on purpose, so it does not clash with an existing local PostgreSQL instance on `5432`.

If you want to use your own local PostgreSQL instead, update `PREPAREME_DATABASE_URL` in `backend/.env` to match your actual credentials and port.

### Useful URLs

- API root: `http://localhost:8000/`
- API docs: `http://localhost:8000/docs`
- Frontend: `http://localhost:3000`

### Test Auth Headers

Protected backend routes currently use development headers:

- `X-PrepareMe-User-Id`
- `X-PrepareMe-Institution-Id`
- `X-PrepareMe-Role`
- `X-PrepareMe-Email`

Example:

```powershell
curl http://localhost:8000/v1/auth/me `
  -H "X-PrepareMe-User-Id: 11111111-1111-1111-1111-111111111111" `
  -H "X-PrepareMe-Institution-Id: aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa" `
  -H "X-PrepareMe-Role: teacher" `
  -H "X-PrepareMe-Email: teacher@prepareme.test"
```

