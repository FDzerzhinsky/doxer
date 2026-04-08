# Backend API Contract

This document captures the backend surface area the frontend and implementation can align on.

## Health

### `GET /health`

Response:

```json
{
  "status": "ok",
  "service": "AI Document Assistant"
}
```

## Documents

### `POST /api/documents/upload`

Form data:

- `file`: PDF or TXT upload

Response:

```json
{
  "document_id": "doc_12345",
  "filename": "employee-handbook.pdf",
  "status": "processed",
  "uploaded_at": "2026-04-08T10:15:00Z",
  "chunks_created": 24,
  "embedding_model": "sentence-transformers/all-MiniLM-L6-v2"
}
```

### `GET /api/documents`

Response:

```json
{
  "documents": [
    {
      "document_id": "doc_12345",
      "filename": "employee-handbook.pdf",
      "status": "processed",
      "uploaded_at": "2026-04-08T10:15:00Z",
      "chunks_created": 24,
      "embedding_model": "sentence-transformers/all-MiniLM-L6-v2"
    }
  ]
}
```

### `GET /api/documents/{document_id}`

Response:

```json
{
  "document_id": "doc_12345",
  "filename": "employee-handbook.pdf",
  "status": "processed",
  "uploaded_at": "2026-04-08T10:15:00Z",
  "chunks_created": 24,
  "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
  "content_type": "application/pdf"
}
```

## Chat

### `POST /api/chat/ask`

Request:

```json
{
  "question": "What is the remote work policy?",
  "document_id": "doc_12345"
}
```

Response:

```json
{
  "question": "What is the remote work policy?",
  "answer": "This is a backend skeleton response.",
  "sources": []
}
```
