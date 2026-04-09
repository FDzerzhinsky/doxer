from __future__ import annotations

import json

import pytest

from app.core.config import Settings
from app.repositories.metadata_store import JsonMetadataStore
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore

from tests.conftest import DummyUploadFile


@pytest.mark.smoke
async def test_text_ingestion_outputs_json_snapshot(tmp_path) -> None:
    settings = Settings(
        upload_dir=tmp_path / "uploads",
        index_path=tmp_path / "index",
        metadata_dir=tmp_path / "metadata",
        chunk_size=90,
        chunk_overlap=20,
    )

    embedding_service = EmbeddingService()
    vector_store = VectorStore(index_dir=settings.index_path, dimension=embedding_service.dimension)
    metadata_store = JsonMetadataStore(settings.metadata_dir)
    document_service = DocumentService(
        settings=settings,
        embedding_service=embedding_service,
        vector_store=vector_store,
        metadata_store=metadata_store,
    )

    sample_text = (
        "Policy update: the assistant stores uploaded text, splits it into chunks, and keeps metadata for each chunk. "
        "This helps us verify the ingestion pipeline before FAISS. "
        "The JSON snapshot should include the document record, chunk list, and the number of vectors written."
    )

    upload = DummyUploadFile(filename="policy.txt", content=sample_text.encode("utf-8"))

    record = await document_service.register_upload(upload)
    chunks = metadata_store.list_chunks(record.document_id)

    snapshot = {
        "document": record.model_dump(mode="json"),
        "chunks": [chunk.model_dump(mode="json") for chunk in chunks],
        "vector_count": len(vector_store.records),
    }

    print(json.dumps(snapshot, indent=2, ensure_ascii=False))

    assert snapshot["document"]["status"] == "processed"
    assert snapshot["document"]["chunks_created"] == len(snapshot["chunks"])
    assert snapshot["vector_count"] == len(snapshot["chunks"])
    assert snapshot["chunks"][0]["chunk_index"] == 1
    assert snapshot["chunks"][0]["text"]
