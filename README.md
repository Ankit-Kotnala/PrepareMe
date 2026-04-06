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
- login-first frontend shell with role-aware dashboards

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

For the current auth-and-dashboard phase, the base migration will gracefully skip `pgvector` if your local PostgreSQL installation does not provide that extension yet. Later retrieval migrations will require a pgvector-enabled database.

### Useful URLs

- API root: `http://localhost:8000/`
- API docs: `http://localhost:8000/docs`
- Frontend: `http://localhost:3000`

### Login Flow

The local app now boots into a real sign-in screen. On backend startup, demo users are automatically seeded into the local database when `PREPAREME_AUTH_MODE=local_jwt` and `PREPAREME_BOOTSTRAP_DEMO_DATA=true`.

Demo credentials:

- Institution code: `prepareme-demo`
- Admin: `admin@prepareme.local` / `Admin@123`
- Teacher: `teacher@prepareme.local` / `Teacher@123`
- Student: `student@prepareme.local` / `Student@123`

For local development, the login surface is protected with Cloudflare Turnstile using Cloudflare's official test site key and secret. Replace those values with real tenant-owned keys before any non-local deployment.

Sign in at `http://localhost:3000` and the app will route each user to the correct dashboard:

- `/teacher` for teacher and course admin roles
- `/student` for students
- `/admin` for institution and platform admins

If login fails with a service-unreachable message, make sure the FastAPI backend is running on `http://localhost:8000`.

