"""
EN: File: app/repositories/metadata_store.py
EN: Purpose: Implements persistence and metadata access operations.
EN: Scope: Documents key classes, functions, and execution flow in two languages.
EN: Notes: Keep comments concise and aligned with implementation changes.
RU: Файл: app/repositories/metadata_store.py
RU: Назначение: Реализует операции доступа к хранилищу и метаданным.
RU: Область: Документирует ключевые классы, функции и поток выполнения на двух языках.
RU: Примечание: Держите комментарии лаконичными и синхронизированными с кодом.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from threading import RLock

from app.models.document import DocumentChunkRecord, DocumentRecord


# EN: Class MetadataSnapshot groups related state and behavior.
# RU: Класс MetadataSnapshot объединяет связанное состояние и поведение.
@dataclass(slots=True)
class MetadataSnapshot:
    documents: dict[str, DocumentRecord]
    chunks: dict[str, list[DocumentChunkRecord]]


# EN: Class JsonMetadataStore groups related state and behavior.
# RU: Класс JsonMetadataStore объединяет связанное состояние и поведение.
class JsonMetadataStore:
    # EN: Method __init__ performs a focused step of the class workflow.
    # RU: Метод __init__ выполняет целевой шаг в рабочем процессе класса.
    def __init__(self, storage_dir: Path) -> None:
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._documents_path = self.storage_dir / "documents.json"
        self._chunks_path = self.storage_dir / "chunks.json"
        self._lock = RLock()
        self._snapshot = self._load_snapshot()

    # EN: Method upsert_document performs a focused step of the class workflow.
    # RU: Метод upsert_document выполняет целевой шаг в рабочем процессе класса.
    def upsert_document(self, document: DocumentRecord) -> None:
        with self._lock:
            self._snapshot.documents[document.document_id] = document
            self._write_documents()

    # EN: Method list_documents performs a focused step of the class workflow.
    # RU: Метод list_documents выполняет целевой шаг в рабочем процессе класса.
    def list_documents(self) -> list[DocumentRecord]:
        with self._lock:
            return list(self._snapshot.documents.values())

    # EN: Method get_document performs a focused step of the class workflow.
    # RU: Метод get_document выполняет целевой шаг в рабочем процессе класса.
    def get_document(self, document_id: str) -> DocumentRecord | None:
        with self._lock:
            return self._snapshot.documents.get(document_id)

    # EN: Method add_chunks performs a focused step of the class workflow.
    # RU: Метод add_chunks выполняет целевой шаг в рабочем процессе класса.
    def add_chunks(self, document_id: str, chunks: list[DocumentChunkRecord]) -> None:
        with self._lock:
            self._snapshot.chunks[document_id] = chunks
            self._write_chunks()

    # EN: Method list_chunks performs a focused step of the class workflow.
    # RU: Метод list_chunks выполняет целевой шаг в рабочем процессе класса.
    def list_chunks(self, document_id: str) -> list[DocumentChunkRecord]:
        with self._lock:
            return list(self._snapshot.chunks.get(document_id, []))

    # EN: Method _load_snapshot performs a focused step of the class workflow.
    # RU: Метод _load_snapshot выполняет целевой шаг в рабочем процессе класса.
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

    # EN: Method _write_documents performs a focused step of the class workflow.
    # RU: Метод _write_documents выполняет целевой шаг в рабочем процессе класса.
    def _write_documents(self) -> None:
        payload = {
            document_id: document.model_dump(mode="json")
            for document_id, document in self._snapshot.documents.items()
        }
        self._documents_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")

    # EN: Method _write_chunks performs a focused step of the class workflow.
    # RU: Метод _write_chunks выполняет целевой шаг в рабочем процессе класса.
    def _write_chunks(self) -> None:
        payload = {
            document_id: [chunk.model_dump(mode="json") for chunk in chunk_list]
            for document_id, chunk_list in self._snapshot.chunks.items()
        }
        self._chunks_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")
