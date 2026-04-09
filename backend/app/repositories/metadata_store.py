from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from threading import RLock

from app.models.document import DocumentChunkRecord, DocumentRecord


@dataclass(slots=True)
class MetadataSnapshot:
    documents: dict[str, DocumentRecord]
    chunks: dict[str, list[DocumentChunkRecord]]


class JsonMetadataStore:
    def __init__(self, storage_dir: Path) -> None:
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._documents_path = self.storage_dir / "documents.json"
        self._chunks_path = self.storage_dir / "chunks.json"
        self._lock = RLock()
        self._snapshot = self._load_snapshot()

    def upsert_document(self, document: DocumentRecord) -> None:
        with self._lock:
            self._snapshot.documents[document.document_id] = document
            self._write_documents()

    def list_documents(self) -> list[DocumentRecord]:
        with self._lock:
            return list(self._snapshot.documents.values())

    def get_document(self, document_id: str) -> DocumentRecord | None:
        with self._lock:
            return self._snapshot.documents.get(document_id)

    def add_chunks(self, document_id: str, chunks: list[DocumentChunkRecord]) -> None:
        with self._lock:
            self._snapshot.chunks[document_id] = chunks
            self._write_chunks()

    def list_chunks(self, document_id: str) -> list[DocumentChunkRecord]:
        with self._lock:
            return list(self._snapshot.chunks.get(document_id, []))

    def _load_snapshot(self) -> MetadataSnapshot:
        documents: dict[str, DocumentRecord] = {}
        chunks: dict[str, list[DocumentChunkRecord]] = {}

        if self._documents_path.exists():
            raw_documents = json.loads(self._documents_path.read_text(encoding="utf-8"))
            documents = {
                document_id: DocumentRecord.model_validate(payload)
                for document_id, payload in raw_documents.items()
            }

        if self._chunks_path.exists():
            raw_chunks = json.loads(self._chunks_path.read_text(encoding="utf-8"))
            chunks = {
                document_id: [DocumentChunkRecord.model_validate(payload) for payload in payloads]
                for document_id, payloads in raw_chunks.items()
            }

        return MetadataSnapshot(documents=documents, chunks=chunks)

    def _write_documents(self) -> None:
        payload = {
            document_id: document.model_dump(mode="json")
            for document_id, document in self._snapshot.documents.items()
        }
        self._documents_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")

    def _write_chunks(self) -> None:
        payload = {
            document_id: [chunk.model_dump(mode="json") for chunk in chunk_list]
            for document_id, chunk_list in self._snapshot.chunks.items()
        }
        self._chunks_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")
