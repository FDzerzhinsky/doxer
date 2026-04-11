# Backend

FastAPI backend for the AI Document Assistant RAG pipeline.

## What is in scope now

- HTTP contract for health, uploads, document listing, and chat
- Configuration and dependency wiring
- JSON-backed metadata storage for documents and chunks, plus a FAISS-backed vector index
- Ollama-backed answer generation with a mock fallback for offline development
- Utility helpers for chunking and document loading

## Current boundaries

- Uploads are persisted to `data/uploads`
- Metadata is persisted to `data/metadata`
- Vector search is backed by FAISS and persisted to `data/index`
- The embedding layer works today, but it uses deterministic hash vectors rather than a semantic model
- The LLM layer can call a local Ollama server; mock mode remains available for offline development
- PDF support depends on `pypdf`

## What works now

- File upload, chunking, and metadata persistence
- Deterministic embeddings for each chunk and query
- FAISS-backed similarity search with on-disk persistence
- Ollama or mock answer generation, depending on environment config

## What is still provisional

- The embedding service is a placeholder and should be swapped for a real model when needed
- The LLM flow currently returns a single non-streaming answer
- Document metadata still uses JSON files, not a database

## Run shape

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Testing

The test layout is layered so each stage catches a different class of bug.

- unit tests cover chunking and file-loading helpers
- service tests cover upload orchestration and vector insertion
- API tests cover FastAPI contracts and dependency wiring

See [docs/testing-strategy.md](../docs/testing-strategy.md) for the full sequence and `uv` commands.

### Inspect chunk output manually

To see the chunk boundaries printed in the terminal, run:

```bash
uv run pytest -s tests/test_chunking_demo.py
```

That test is intentionally small and prints the resulting chunks so you can verify the slicing logic by eye.

### Inspect JSON ingestion snapshot

To feed text through the ingestion pipeline and print the resulting document metadata plus chunk list as JSON, run:

```bash
uv run pytest -s tests/test_ingestion_snapshot.py
```

This is the quickest way to confirm that upload, chunking, embedding, and metadata persistence are all wired together.

### Inspect your own file

You can point the backend at your own local TXT, MD, or PDF file and print the resulting JSON snapshot with:

```bash
uv run inspect-ingestion --file path/to/your-file.txt
```

If you want to keep the generated files instead of using a temporary workspace, add:

```bash
uv run inspect-ingestion --file path/to/your-file.txt --workspace-dir data/inspection
```

The output includes the source file path, the workspace used for uploads and metadata, the document record, the chunk list, and the number of vectors created.

### Ask a question about your file

To ingest a local file and ask a question against it from the command line, run:

```bash
uv run --project backend ask-document --file path/to/your-file.txt --llm-provider mock --question "Найди в документе упоминание того-то"
```

If you are already inside `backend/`, you can omit `--project backend` and use `uv run ask-document ...` instead.
Recommended model for an RTX 3080 with 10 GB VRAM: `qwen2.5:7b`. It is small enough to run comfortably on this GPU and supports Russian well.

`mock` means the answer is generated without calling Ollama. It is useful for offline checks and for testing the retrieval path without requiring a local model server.

If `LLM_PROVIDER=ollama`, the answer will come from your local Ollama server. To use that path, Ollama must be installed, running, and have the target model pulled locally.

The command prints a JSON payload with the question, the answer, the retrieved sources, and the ingestion snapshot.

## Notes for the next iteration

1. Add streaming responses for Ollama.
2. Move metadata persistence to a real database-backed store.
3. Add tests around upload, chunking, retrieval, and LLM fallbacks.
