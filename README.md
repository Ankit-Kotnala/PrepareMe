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

