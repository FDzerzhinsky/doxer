from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import Settings
from app.models.document import DocumentRecord
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorRecord, VectorStore
from app.utils.chunking import chunk_text
from app.utils.file_loader import load_document_text


class DocumentService:
    def __init__(self, settings: Settings, embedding_service: EmbeddingService, vector_store: VectorStore) -> None:
        self.settings = settings
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self._documents: dict[str, DocumentRecord] = {}

    async def register_upload(self, file: UploadFile) -> DocumentRecord:
        document_id = f"doc_{uuid4().hex[:12]}"
        file_path = self.settings.upload_dir / f"{document_id}_{Path(file.filename).name}"

        content = await file.read()
        file_path.write_bytes(content)

        extracted_text = load_document_text(file_path)
        chunks = chunk_text(
            extracted_text,
            chunk_size=self.settings.chunk_size,
            overlap=self.settings.chunk_overlap,
        )

        embeddings = self.embedding_service.embed_texts(chunks)
        for index, (chunk_text_value, embedding) in enumerate(zip(chunks, embeddings, strict=False), start=1):
            self.vector_store.upsert(
                VectorRecord(
                    chunk_id=f"{document_id}_chunk_{index}",
                    document_id=document_id,
                    text=chunk_text_value,
                    embedding=embedding,
                )
            )

        record = DocumentRecord(
            document_id=document_id,
            filename=file.filename,
            status="processed",
            uploaded_at=datetime.now(UTC),
            chunks_created=len(chunks),
            embedding_model=self.settings.embedding_model,
            content_type=file.content_type,
            file_path=file_path,
        )
        self._documents[document_id] = record
        return record

    def list_documents(self) -> list[DocumentRecord]:
        return list(self._documents.values())

    def get_document(self, document_id: str) -> DocumentRecord | None:
        return self._documents.get(document_id)
