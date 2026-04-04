# PrepareMe Execution Playbook
### The build format for turning the blueprint into a scalable, lovable product

---

## Purpose

This document translates the vision in `PrepareMe_Blueprint.md` and the engineering guardrails in `PrepareMe_Codex_Prompt.md` into an execution format we can actually build from.

Use the three documents like this:

- `PrepareMe_Blueprint.md`: vision, category thesis, moat, market, product strategy
- `PrepareMe_Codex_Prompt.md`: coding rules, architecture guardrails, security posture
- `PrepareMe_Execution_Playbook.md`: build order, repo shape, delivery format, and scale plan

If the blueprint says **what PrepareMe is**, this playbook says **how we build it well**.

---

## North Star

PrepareMe wins if it becomes the most trusted and most operationally useful AI learning system for institutions.

That means every release should strengthen at least one of these:

1. The curriculum graph
2. The mastery memory
3. The institutional policy engine
4. The teacher control plane
5. The hallucination firewall

If a feature does not strengthen one of these, it should be small, cheap, and deprioritized.

---

## What "Best Way Possible" Means

For PrepareMe, the best way is not maximum complexity. It is disciplined sequencing.

We optimize for:

- Trust before novelty
- Data structure before UI flourish
- Workflow depth before feature breadth
- Tenant isolation before convenience
- Measurable learning outcomes before AI theatrics
- Fast monolith execution before distributed-system vanity

The product should feel:

- Grounded: answers come from approved institutional material
- Fast: the common path feels near-instant
- Personal: the system clearly remembers the student
- Governed: teachers remain in control
- Predictable: institutions can audit what happened and why

---

## Non-Negotiables

These are always true, even in MVP:

- Every tenant-scoped table carries `institution_id`
- Every query explicitly scopes by `institution_id`
- PostgreSQL RLS is enabled for tenant tables
- All AI output is logged
- Student-facing generated assessments go through approval workflow
- All LLM calls go through the provider adapter
- All vector retrieval is pre-filtered by tenant
- S3 object paths are tenant-scoped
- Wrong-tenant tests exist for tenant-touching code
- Prompt construction is layered, not hardcoded

---

## Product Pillars

### Pillar 1: Trust

Trust is built through:

- curriculum-aware scope checking
- hybrid retrieval with reranking
- confidence scoring and refusal modes
- source citations
- immutable audit logs
- teacher approval workflows

If trust breaks, the product breaks.

### Pillar 2: Compounding Memory

PrepareMe must get better with continued usage.

Compounding comes from:

- student mastery updates
- forgetting decay tracking
- confusion tags
- cohort-level aggregation
- institution-specific policy tuning
- exam-style learning over time

### Pillar 3: Teacher Leverage

Teachers should save real time every week.

The teacher experience must turn:

- uploads into mapped content
- mapped content into draft assessments
- drafts into reviewed, publishable assets
- student activity into usable intervention signals

### Pillar 4: Institutional Defensibility

Institutions stay when:

- their curriculum graph is encoded
- their teacher workflows live in the product
- their students' mastery history compounds
- their admins rely on analytics and policy controls

---

## Build Order

Build in this order. Do not skip layers.

### Phase 0: Foundation

Goal: create a secure, typed, multi-tenant-ready substrate.

Build:

- FastAPI monolith with internal modules
- Next.js app shell with role-aware routing
- PostgreSQL schema baseline
- RLS policies and institution context middleware
- Clerk auth integration
- Structlog + Sentry
- Redis + Celery
- S3/R2 storage abstraction
- provider adapter interface for LLM and embeddings
- basic CI with linting, typing, tests

Exit criteria:

- authenticated requests resolve institution context correctly
- wrong-tenant access fails consistently
- LLM calls are only possible through the adapter
- audit logging infrastructure exists

### Phase 1: Curriculum Graph + Ingestion

Goal: turn raw academic assets into structured institutional data.

Build:

- document upload flow
- ingestion job pipeline
- text extraction for PDF/DOCX/PPTX
- semantic chunking
- curriculum node creation and manual editing UI
- AI-assisted chunk-to-node mapping
- versioning and provenance metadata

Exit criteria:

- one institution can upload real documents
- chunks are created with provenance and node references
- teachers can correct graph structure manually

### Phase 2: Hallucination Firewall

Goal: make grounded Q&A better than a generic chatbot.

Build:

- scope checker
- dense retrieval via pgvector
- sparse retrieval via PostgreSQL full-text search
- RRF merge
- curriculum-aware filtering
- cross-encoder reranking
- confidence scoring
- refusal logic
- explanation mode with citations
- full `ai_interactions` logging

Exit criteria:

- common in-scope questions answer with citations
- low-confidence questions hedge or refuse correctly
- out-of-scope questions short-circuit without LLM generation

### Phase 3: Teacher Control Plane

Goal: save teacher time and create workflow lock-in.

Build:

- upload review queue
- content approval workflow
- AI-generated quiz drafts
- teacher edit and approval flow
- publish flow
- tenant policy settings v1

Exit criteria:

- teacher can go from upload to approved quiz in one coherent flow
- audit trail exists for generation, approval, rejection, and publication

### Phase 4: Mastery Memory

Goal: make PrepareMe feel personalized and compounding.

Build:

- persistent mastery records
- mastery update engine from attempts and interactions
- forgetting decay logic
- confusion tags
- revision recommendations
- student learning debt summary

Exit criteria:

- repeat student sessions adapt based on prior activity
- weak areas are visible and actionable

### Phase 5: Analytics and Institutional Value

Goal: make the product valuable to admins and academic leadership.

Build:

- cohort weak-topic heatmaps
- class-level confusion clustering
- exam readiness scoring
- content effectiveness signals
- reporting and exports

Exit criteria:

- admins can identify risk patterns before exam outcomes arrive

### Phase 6: Intelligence Layer

Goal: deepen the moat after the data foundations are strong.

Build:

- Exam Twin Engine
- advanced remediation
- Socratic viva
- multilingual academic explanations
- LMS integration hooks
- enterprise SSO

Exit criteria:

- advanced features are built on clean V1 data, not guesswork

---

## What To Delay On Purpose

Delay these until the core loop is excellent:

- native mobile apps
- voice-native experiences
- cross-tenant intelligence
- marketplace concepts
- microservices
- separate analytics or vector databases
- highly bespoke customer-specific branches

These are not bad ideas. They are just not first-order leverage.

---

## System Shape

### Architecture Principle

Monolith first. Strong modules. Async edges. Event-driven background work where it matters.

### Backend Modules

- `auth/`: JWT verification, RBAC, request context, institution enforcement
- `curriculum/`: ingestion, graph, node mapping, provenance, versioning
- `retrieval/`: scope check, hybrid search, rerank, confidence, refusal
- `assessment/`: quiz and exam generation, approval lifecycle, attempts
- `memory/`: mastery, forgetting, confusion, revision logic
- `policies/`: tenant policies, strictness, approval rules, retrieval configuration
- `analytics/`: cohort insights, clustering, readiness, scheduled aggregates
- `admin/`: institution settings, reporting, audits, platform controls
- `core/`: config, db, logging, storage, task orchestration, shared types

### Hot Path

The hot path is the user-facing request path and must stay small:

1. authenticate
2. resolve institution context
3. scope check
4. retrieve
5. rerank
6. confidence evaluation
7. generate or refuse
8. log
9. return

Everything else should move to async jobs.

### Async Path

Use Celery for:

- document extraction
- embedding generation
- graph mapping
- bulk re-indexing
- analytics aggregation
- notification delivery
- content drift detection
- mastery recomputation jobs

---

## Repo Format

Target structure:

```text
prepareme/
  apps/
    api/
    web/
  backend/
    app/
      api/
      auth/
      curriculum/
      retrieval/
      assessment/
      memory/
      policies/
      analytics/
      admin/
      core/
    tests/
    alembic/
  frontend/
    app/
    components/
    features/
    lib/
    hooks/
    stores/
  infra/
    docker/
    scripts/
  docs/
    architecture/
    product/
    runbooks/
```

Rules:

- keep domain logic out of route handlers
- keep provider SDK calls out of business services
- keep tenant enforcement visible in service signatures
- keep schema and migration changes explicit and reviewed

---

## Data Design Rules

### Transactional Data

PostgreSQL is the source of truth for:

- institutions
- users
- courses
- curriculum graph
- documents and chunks
- mastery records
- assessments and attempts
- policies
- AI interactions

### Append-Only Data

Treat these as append-only or append-dominant from the beginning:

- `ai_interactions`
- event-like audit logs
- ingestion job records
- assessment attempt history

Design them to be partition-friendly once volume grows.

### Versioning

Version these explicitly:

- curriculum nodes
- documents
- embeddings
- prompts and policy snapshots
- exam style models

If a model output matters later, save the version context that produced it.

---

## Performance Strategy

### User-Visible Targets

Initial targets:

- explanation mode p50 under 1.5s
- explanation mode p95 under 3.0s
- scope check under 10ms
- retrieval plus rerank under 350ms on common queries
- teacher upload acknowledgment under 1s, with async processing after

### Performance Principles

- pre-filter by tenant and course before expensive retrieval
- cache stable curriculum graph reads
- avoid synchronous file parsing on request path
- avoid N+1 queries in dashboards
- use background jobs for embedding and analytics work
- use server-side pagination everywhere admin data can grow
- optimize the top five hottest queries before chasing broad tuning

---

## Scalability Strategy

### Stage 1: 1 to 5 Institutions

Optimize for speed of learning, not infra sophistication.

- single PostgreSQL instance
- pgvector in the same database
- single Redis
- single worker pool
- monolith deploy on Railway or Render

### Stage 2: 5 to 30 Institutions

Optimize for reliability and observability.

- move containerized workloads to AWS
- separate web and worker scaling
- introduce read replicas only if needed
- add job queues by workload class if contention appears
- start partitioning heavy audit tables

### Stage 3: 30+ Institutions

Optimize for workload isolation and cost control.

- dedicated worker queues for ingestion vs analytics
- stronger caching around graph and reporting reads
- tenant-aware rate limiting
- storage lifecycle policies
- optional enterprise isolation for special contracts

### Stage 4: Enterprise Expansion

Optimize for compliance and operational rigor.

- SSO
- fine-grained audit access
- data retention controls
- regional deployment strategy only when contractually required

---

## Product Experience Rules

If users are going to love PrepareMe, these rules matter as much as architecture.

### Student Experience

- always show citations when answering from content
- when refusing, explain why and what the student can do next
- make progress visible through mastery and revision signals
- keep the interface calm and academic, not gimmicky
- prioritize clarity over cleverness

### Teacher Experience

- reduce clicks in the review queue
- surface low-confidence generations clearly
- let teachers override mappings and policies without engineering help
- make approvals and rejections traceable
- turn every upload into something useful quickly

### Admin Experience

- show actionable trends, not vanity charts
- make cohort weakness obvious
- connect analytics to curriculum nodes, not generic labels
- separate individual insight from institutional reporting cleanly

---

## Engineering Operating Rules

### Every Task Must Be Written In This Format

When scoping work, use this template:

1. Objective
2. Module
3. User outcome
4. Tenant isolation implications
5. Audit logging implications
6. Data model changes
7. API changes
8. UI changes
9. Background jobs
10. Metrics and observability
11. Tests, including wrong-tenant case
12. Rollout and feature flag strategy

### Every PR Must Answer

1. What moat does this strengthen?
2. How is tenant isolation enforced?
3. What gets logged?
4. What happens when confidence is low or data is missing?
5. What is the failure mode?
6. What tests prove the wrong-tenant path is safe?

### Definition of Done

A feature is not done until:

- typed schemas exist
- tenant enforcement is explicit
- audit logging is in place
- feature behavior is policy-aware where required
- tests cover success, failure, and wrong-tenant cases
- metrics or logs are sufficient to debug production behavior
- docs are updated if behavior or architecture changed

---

## Evaluation Discipline

PrepareMe should never ship AI changes without evaluation.

Track:

- answer accuracy
- citation precision
- refusal correctness
- retrieval recall at K
- low-confidence false positive rate
- latency p50 and p95
- teacher approval rate on generated content
- student repeat usage on mastery-driven features

The evaluation harness should be treated as product infrastructure, not an optional QA step.

---

## Decision Filter

Use this filter before building anything:

### Build It Now If

- it improves trust
- it strengthens the curriculum graph
- it compounds mastery memory
- it saves teacher time repeatedly
- it improves tenant safety or auditability

### Delay It If

- it is demo-good but workflow-weak
- it depends on data we do not yet have
- it introduces operational complexity early
- it makes the system harder to reason about
- it cannot be expressed cleanly in tenant policy

---

## Suggested First 90 Days

### Days 1 to 15

- set up repo and monolith foundations
- auth, institution context, RLS, logging, storage
- create base schema and migrations
- establish CI, linting, typing, test scaffolding

### Days 16 to 30

- upload pipeline
- extraction and chunking
- curriculum node CRUD and mapping UI
- provenance model

### Days 31 to 45

- hybrid retrieval
- reranking
- confidence scoring
- refusal flow
- explanation mode

### Days 46 to 60

- teacher review queue
- quiz draft generation
- approval and publish workflow
- tenant policy settings v1

### Days 61 to 75

- mastery record persistence
- mastery delta updates from attempts
- learning debt summary
- revision recommendations

### Days 76 to 90

- cohort analytics v1
- operational hardening
- evaluation harness expansion
- pilot onboarding support

---

## Final Rule

PrepareMe should never feel like "AI sprinkled on top."

It should feel like the institution's curriculum has become executable:

- searchable
- governable
- measurable
- personalized
- and compounding over time

That is the standard.

