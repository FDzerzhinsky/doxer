from __future__ import annotations

from datetime import datetime, timezone
import mimetypes
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import Settings
from app.models.document import DocumentChunkRecord, DocumentRecord
from app.repositories.metadata_store import JsonMetadataStore
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorRecord, VectorStore
from app.utils.chunking import chunk_text
from app.utils.file_loader import load_document_text


class DocumentService:
    def __init__(
        self,
        settings: Settings,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
        metadata_store: JsonMetadataStore,
    ) -> None:
        self.settings = settings
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.metadata_store = metadata_store
        self._documents: dict[str, DocumentRecord] = {}
        self.settings.ensure_directories()
        self._load_documents_from_store()

    async def register_upload(self, file: UploadFile) -> DocumentRecord:
        content = await file.read()
        return self._register_bytes(
            filename=file.filename,
            content=content,
            content_type=file.content_type,
        )

    def register_local_file(self, source_path: Path) -> DocumentRecord:
        if not source_path.exists():
            raise FileNotFoundError(source_path)

        return self._register_bytes(
            filename=source_path.name,
            content=source_path.read_bytes(),
            content_type=mimetypes.guess_type(source_path.name)[0],
        )

    def list_documents(self) -> list[DocumentRecord]:
        return list(self._documents.values())

    def get_document(self, document_id: str) -> DocumentRecord | None:
        return self._documents.get(document_id)

    def build_document_snapshot(self, document_id: str) -> dict[str, object]:
        document = self.get_document(document_id)
        if document is None:
            raise KeyError(f"Document not found: {document_id}")

        chunk_records = self.metadata_store.list_chunks(document_id)
        vector_records = [record for record in self.vector_store.records if record.document_id == document_id]

        return {
            "document": document.model_dump(mode="json"),
            "chunks": [chunk.model_dump(mode="json") for chunk in chunk_records],
            "vector_count": len(vector_records),
        }

    def _load_documents_from_store(self) -> None:
        for document in self.metadata_store.list_documents():
            self._documents[document.document_id] = document

    def _register_bytes(self, filename: str, content: bytes, content_type: str | None) -> DocumentRecord:
        document_id = f"doc_{uuid4().hex[:12]}"
        file_path = self.settings.upload_dir / f"{document_id}_{Path(filename).name}"

        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(content)

        extracted_text = load_document_text(file_path)
        chunks = chunk_text(
            extracted_text,
            chunk_size=self.settings.chunk_size,
            overlap=self.settings.chunk_overlap,
        )

        embeddings = self.embedding_service.embed_texts(chunks)
        chunk_records: list[DocumentChunkRecord] = []
        for index, (chunk_text_value, embedding) in enumerate(zip(chunks, embeddings, strict=False), start=1):
            chunk_record = DocumentChunkRecord(
                chunk_id=f"{document_id}_chunk_{index}",
                document_id=document_id,
                chunk_index=index,
                text=chunk_text_value,
                character_count=len(chunk_text_value),
            )
            chunk_records.append(chunk_record)
            self.vector_store.upsert(
                VectorRecord(
                    chunk_id=chunk_record.chunk_id,
                    document_id=document_id,
                    text=chunk_record.text,
                    embedding=embedding,
                )
            )

        record = DocumentRecord(
            document_id=document_id,
            filename=filename,
            status="processed",
            uploaded_at=datetime.now(timezone.utc),
            chunks_created=len(chunks),
            embedding_model=self.settings.embedding_model,
            content_type=content_type,
            file_path=file_path,
        )
        self._documents[document_id] = record
        self.metadata_store.upsert_document(record)
        self.metadata_store.add_chunks(document_id, chunk_records)
        return record
