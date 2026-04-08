# Backend

FastAPI backend for the AI Document Assistant RAG pipeline.

## What is in scope now

- HTTP contract for health, uploads, document listing, and chat
- Configuration and dependency wiring
- In-memory service skeletons that can be replaced with real persistence and FAISS later
- Utility helpers for chunking and document loading

## Current boundaries

- Uploads are persisted to `data/uploads`
- Vector search is in-memory for now
- The LLM layer is a placeholder that returns a deterministic skeleton response
- PDF support depends on `pypdf`

## Run shape

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Notes for the next iteration

1. Replace the in-memory vector store with FAISS.
2. Swap the placeholder LLM service for Ollama or a hosted model API.
3. Move document persistence to a real metadata store.
4. Add tests around upload, chunking, and retrieval paths.
