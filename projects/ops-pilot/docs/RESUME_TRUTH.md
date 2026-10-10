# Resume Truth Table

This file separates what is inherited, what is modified, and what has actually been verified locally.

## Current status

- Inherited source: original multi-agent/RAG architecture is retained for study; full production startup is not claimed.
- Personal code changes: Lite Mode implementation and documentation are committed on `personal/ops-pilot`.
- Local end-to-end verification: Lite Mode has been verified through routing, local retrieval, evidence collection, and one DeepSeek report-generation request.
- Docker/Milvus/Redis/PostgreSQL verification: not performed.
- Ollama `bge-m3` availability: verified before project setup.
- Existing local support: FAISS and Ollama/LangChain adapters are already available in `agent_study_env`.
- Full API startup: not verified; current `app.main` expects Milvus and may initialize PostgreSQL/Redis.
- Full `requirements.txt`: not installed.

## Personally added and verified

- Added a `Lite Mode` LangGraph path for single-machine development without Docker, Milvus, Redis, or PostgreSQL.
- Added a local FAISS retrieval adapter using the existing Ollama `bge-m3` embedding model.
- Added a transparent candidate pre-filter for constrained local indexing.
- Added an evidence record shape (`evidence_id`, kind, source, content, confidence) and a report fallback that discloses degraded dependencies.
- Verified: LangGraph state flow without RAG/API.
- Verified: local Ollama embedding and FAISS retrieval for an OOM/memory-pressure query.
- Verified: one DeepSeek report-generation request through Lite Mode.
- Not yet verified: original FastAPI API, Milvus, Redis, PostgreSQL, MCP services, Workers, full-corpus retrieval, or the original deep diagnosis graph.

## Resume rule

Only claim a feature as implemented and verified after the code change and a reproducible check are recorded in `PROJECT_WORKLOG.md`.

Do not claim full deployment, high-concurrency testing, or production readiness unless those items are actually tested and documented.
