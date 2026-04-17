"""
EN: File: tests/test_document_service.py
EN: Purpose: Contains automated tests validating application behavior and edge cases.
EN: Scope: Documents key classes, functions, and execution flow in two languages.
EN: Notes: Keep comments concise and aligned with implementation changes.
RU: Файл: tests/test_document_service.py
RU: Назначение: Содержит автотесты, проверяющие поведение приложения и граничные случаи.
RU: Область: Документирует ключевые классы, функции и поток выполнения на двух языках.
RU: Примечание: Держите комментарии лаконичными и синхронизированными с кодом.
"""

from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.repositories.metadata_store import JsonMetadataStore
from app.services.vector_store import VectorStore

from tests.conftest import DummyUploadFile


# EN: Function test_register_upload_processes_file_and_chunks executes a specific reusable operation.
# RU: Функция test_register_upload_processes_file_and_chunks выполняет конкретную переиспользуемую операцию.
async def test_register_upload_processes_file_and_chunks(test_settings) -> None:
    embedding_service = EmbeddingService()
    vector_store = VectorStore(index_dir=test_settings.index_path, dimension=embedding_service.dimension)
    metadata_store = JsonMetadataStore(test_settings.metadata_dir)
    service = DocumentService(
        settings=test_settings,
        embedding_service=embedding_service,
        vector_store=vector_store,
        metadata_store=metadata_store,
    )

    upload = DummyUploadFile(
        filename="policy.txt",
        content=b"alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu",
    )

    record = await service.register_upload(upload)

    assert record.status == "processed"
    assert record.chunks_created >= 2
    assert record.file_path is not None
    assert record.file_path.exists()
    assert len(vector_store.records) == record.chunks_created
    assert service.get_document(record.document_id) == record


# EN: Function test_metadata_persists_between_service_instances executes a specific reusable operation.
# RU: Функция test_metadata_persists_between_service_instances выполняет конкретную переиспользуемую операцию.
async def test_metadata_persists_between_service_instances(test_settings) -> None:
    embedding_service = EmbeddingService()
    vector_store = VectorStore(index_dir=test_settings.index_path, dimension=embedding_service.dimension)
    metadata_store = JsonMetadataStore(test_settings.metadata_dir)

    first_service = DocumentService(
        settings=test_settings,
        embedding_service=embedding_service,
        vector_store=vector_store,
        metadata_store=metadata_store,
    )

    upload = DummyUploadFile(
        filename="guide.txt",
        content=b"first line second line third line fourth line fifth line",
    )

    record = await first_service.register_upload(upload)

    second_service = DocumentService(
        settings=test_settings,
        embedding_service=embedding_service,
        vector_store=vector_store,
        metadata_store=JsonMetadataStore(test_settings.metadata_dir),
    )

    loaded_record = second_service.get_document(record.document_id)

    assert loaded_record is not None
    assert loaded_record.document_id == record.document_id
    assert second_service.list_documents()


# EN: Function test_register_local_file_builds_snapshot executes a specific reusable operation.
# RU: Функция test_register_local_file_builds_snapshot выполняет конкретную переиспользуемую операцию.
def test_register_local_file_builds_snapshot(test_settings, tmp_path) -> None:
    embedding_service = EmbeddingService()
    vector_store = VectorStore(index_dir=test_settings.index_path, dimension=embedding_service.dimension)
    metadata_store = JsonMetadataStore(test_settings.metadata_dir)
    service = DocumentService(
        settings=test_settings,
        embedding_service=embedding_service,
        vector_store=vector_store,
        metadata_store=metadata_store,
    )

    source_file = tmp_path / "inspection.txt"
    source_file.write_text(
        "First paragraph about the inspection flow. Second paragraph with more text for chunking. Third paragraph closes the sample.",
        encoding="utf-8",
    )

    record = service.register_local_file(source_file)
    snapshot = service.build_document_snapshot(record.document_id)

    assert snapshot["document"]["filename"] == "inspection.txt"
    assert snapshot["document"]["status"] == "processed"
    assert snapshot["chunks"]
    assert snapshot["chunks"][0]["chunk_index"] == 1
    assert snapshot["vector_count"] == len(snapshot["chunks"])
