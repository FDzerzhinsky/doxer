# Testing Strategy

This project should be tested in layers, from the smallest pure functions to the HTTP surface.

## Tooling

- `uv` manages the backend environment and installs dependencies.
- `pytest` runs the suite.
- `pytest-asyncio` supports async service tests.
- `httpx` powers the FastAPI test client through Starlette.

## Phased Approach

### Phase 1: Pure Unit Tests

Test fast, deterministic code that has no I/O.

- text chunking
- file-type decisions
- small utility helpers

Goal: catch logic bugs without booting the app.

### Phase 2: Service-Level Tests

Test business logic with in-memory dependencies.

- document upload orchestration
- extraction and chunk creation
- vector-store insertion
- response composition in the RAG service

Goal: verify the pipeline before integrating HTTP or persistence.

### Phase 3: API Integration Tests

Test the FastAPI routes using a test client.

- health endpoint
- upload endpoint
- document listing and detail endpoints
- chat endpoint

Goal: validate request/response contracts and dependency wiring.

### Phase 4: Regression and Smoke Tests

Keep a tiny set of checks for CI and local sanity runs.

- app starts
- `/health` returns `ok`
- upload flow still works with a sample TXT file

Goal: detect broken boot paths quickly.

## Run Commands with `uv`

From the `backend/` directory:

```bash
uv sync
uv run pytest
uv run pytest tests/test_chunking.py
uv run pytest -m smoke
uv run ask-document-ollama --file ../docs/example.txt --question "Каким шрифтом следует оформлять название статьи?"
```

The last command is the quickest manual check for the full RAG + LLM path against the bundled sample document.

## Suggested Markers

- `unit` for pure functions and helpers
- `integration` for services and API flow
- `smoke` for the shortest verification path

## What We Verify First

The first stable suite should cover:

1. chunking rules
2. document upload persistence
3. chunk generation and embedding insertion
4. API contracts for upload, list, detail, and chat

That gives the best balance between speed and confidence for this codebase.
