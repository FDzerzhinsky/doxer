# Backend

FastAPI backend for the AI Document Assistant RAG pipeline.

## What is in scope now

- HTTP contract for health, uploads, document listing, and chat
- Configuration and dependency wiring
- JSON-backed metadata storage for documents and chunks, plus a FAISS-backed vector index
- Utility helpers for chunking and document loading

## Current boundaries

- Uploads are persisted to `data/uploads`
- Metadata is persisted to `data/metadata`
- Vector search is backed by FAISS and persisted to `data/index`
- The LLM layer is a placeholder that returns a deterministic skeleton response
- PDF support depends on `pypdf`

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

## Notes for the next iteration

1. Swap the placeholder LLM service for Ollama or a hosted model API.
2. Move metadata persistence to a real database-backed store.
3. Add tests around upload, chunking, and retrieval paths.
