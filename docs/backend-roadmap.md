# Backend Roadmap

This is the order in which the backend should evolve from the current skeleton.

## Current Status

- [x] Phase 1: Skeleton
- [x] Phase 2: Document Processing
- [x] Phase 3: Retrieval
- [x] Phase 4: Model Integration
- [ ] Phase 5: Production Hardening

## Phase 1: Skeleton

- FastAPI app and route wiring
- Settings and dependency injection
- In-memory document registry
- Stub chat response flow

## Phase 2: Document Processing

- Text extraction for TXT and PDF
- Chunking logic integrated into upload processing
- Chunk metadata stored per document

## Phase 3: Retrieval

- FAISS-backed vector store with disk persistence
- Persist embeddings on disk
- Add retrieval scoring and source citation payloads

## Phase 4: Model Integration

- Ollama provider wired into the RAG flow
- Add prompt templates for grounded answers
- Handle error and fallback paths explicitly

## Phase 5: Production Hardening

- Add tests for API and services
- Add structured logging
- Add auth and document isolation
- Add migration path for persistent metadata storage
