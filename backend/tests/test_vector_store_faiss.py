"""
EN: File: tests/test_vector_store_faiss.py
EN: Purpose: Contains automated tests validating application behavior and edge cases.
EN: Scope: Documents key classes, functions, and execution flow in two languages.
EN: Notes: Keep comments concise and aligned with implementation changes.
RU: Файл: tests/test_vector_store_faiss.py
RU: Назначение: Содержит автотесты, проверяющие поведение приложения и граничные случаи.
RU: Область: Документирует ключевые классы, функции и поток выполнения на двух языках.
RU: Примечание: Держите комментарии лаконичными и синхронизированными с кодом.
"""

from app.services.vector_store import VectorRecord, VectorStore


# EN: Function test_vector_store_search_orders_by_similarity executes a specific reusable operation.
# RU: Функция test_vector_store_search_orders_by_similarity выполняет конкретную переиспользуемую операцию.
def test_vector_store_search_orders_by_similarity(tmp_path) -> None:
    store = VectorStore(index_dir=tmp_path / "index", dimension=3)

    store.upsert(
        VectorRecord(
            chunk_id="chunk-1",
            document_id="doc-1",
            text="alpha",
            embedding=[1.0, 0.0, 0.0],
        )
    )
    store.upsert(
        VectorRecord(
            chunk_id="chunk-2",
            document_id="doc-1",
            text="beta",
            embedding=[0.0, 1.0, 0.0],
        )
    )
    store.upsert(
        VectorRecord(
            chunk_id="chunk-3",
            document_id="doc-2",
            text="gamma",
            embedding=[0.0, 0.0, 1.0],
        )
    )

    results = store.search([0.9, 0.1, 0.0], limit=3)

    assert [record.chunk_id for record, _ in results][:2] == ["chunk-1", "chunk-2"]
    assert results[0][1] >= results[1][1]


# EN: Function test_vector_store_reloads_from_disk executes a specific reusable operation.
# RU: Функция test_vector_store_reloads_from_disk выполняет конкретную переиспользуемую операцию.
def test_vector_store_reloads_from_disk(tmp_path) -> None:
    index_dir = tmp_path / "index"
    first_store = VectorStore(index_dir=index_dir, dimension=3, embedding_signature="provider-a:model-a")

    first_store.upsert(
        VectorRecord(
            chunk_id="chunk-9",
            document_id="doc-9",
            text="persisted",
            embedding=[0.0, 1.0, 0.0],
        )
    )

    second_store = VectorStore(index_dir=index_dir, dimension=3, embedding_signature="provider-a:model-a")
    results = second_store.search([0.0, 1.0, 0.0], limit=1)

    assert (index_dir / "vectors.faiss").exists()
    assert (index_dir / "vectors.json").exists()
    assert (index_dir / "vectors.meta.json").exists()
    assert len(second_store.records) == 1
    assert results[0][0].chunk_id == "chunk-9"


# EN: Function test_vector_store_reembeds_when_signature_changes executes a specific reusable operation.
# RU: Функция test_vector_store_reembeds_when_signature_changes выполняет конкретную переиспользуемую операцию.
def test_vector_store_reembeds_when_signature_changes(tmp_path) -> None:
    index_dir = tmp_path / "index"
    original_store = VectorStore(index_dir=index_dir, dimension=2, embedding_signature="provider-a:model-a")

    original_store.upsert(
        VectorRecord(
            chunk_id="chunk-1",
            document_id="doc-1",
            text="alpha",
            embedding=[1.0, 0.0],
        )
    )
    original_store.upsert(
        VectorRecord(
            chunk_id="chunk-2",
            document_id="doc-1",
            text="beta",
            embedding=[0.0, 1.0],
        )
    )

    def reembed(texts: list[str]) -> list[list[float]]:
        lookup = {
            "alpha": [0.0, 1.0],
            "beta": [1.0, 0.0],
        }
        return [lookup[text] for text in texts]

    migrated_store = VectorStore(
        index_dir=index_dir,
        dimension=2,
        embedding_signature="provider-b:model-b",
        reembed_texts=reembed,
    )

    results = migrated_store.search([0.0, 1.0], limit=1)

    assert len(migrated_store.records) == 2
    assert migrated_store.records[0].embedding == [0.0, 1.0]
    assert results[0][0].chunk_id == "chunk-1"
