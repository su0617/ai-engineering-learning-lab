# Lite Mode

Lite Mode is the local development path added for learning and interview preparation.

## Why it exists

The full API entrypoint intentionally initializes Milvus and, when the incident pipeline is enabled, PostgreSQL and Redis. That is useful for the original production-shaped architecture but unnecessary for understanding the Agent loop.

Lite Mode keeps the important flow visible:

```text
route -> retrieve -> collect_evidence -> synthesize -> finalize
```

It uses:

- LangGraph for state transitions
- FAISS for a local vector index
- Ollama `bge-m3` for embeddings
- Read-only local evidence collection
- DeepSeek API when `DEEPSEEK_API_KEY` is configured
- A deterministic report fallback when the API is unavailable

The original Milvus, Redis, PostgreSQL, MCP, FastAPI, fast/deep graph, and Worker code remains in the repository as the complete architecture reference.

## Run without an API key

First verify only graph state transitions:

```powershell
python -m app.lite.cli "我电脑最近很卡" --skip-rag
```

Then verify local RAG with the existing Ollama model:

```powershell
python -m app.lite.cli "主机内存压力和 OOM 怎么排查" --max-docs 20
```

The first RAG run calls Ollama and builds an in-memory FAISS index. It does not create a persistent database or download a new model.

To keep the first run small without letting file order dominate results, Lite Mode applies a transparent keyword pre-filter before embedding a limited number of documents. This is a local-development optimization, not a replacement for the upstream Milvus hybrid retrieval path.

## Run with DeepSeek

Put the key only in a local `.env` file (never commit it):

```env
DEEPSEEK_API_KEY=your-key
LITE_LLM_PROVIDER=deepseek
LITE_LLM_MODEL=deepseek-chat
```

Then run the same command. If the API is unavailable, Lite Mode returns a deterministic report and records the degradation instead of hiding the failure.
