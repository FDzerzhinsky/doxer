from app.services.vector_store import VectorRecord, VectorStore


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


def test_vector_store_reloads_from_disk(tmp_path) -> None:
    index_dir = tmp_path / "index"
    first_store = VectorStore(index_dir=index_dir, dimension=3)

    first_store.upsert(
        VectorRecord(
            chunk_id="chunk-9",
            document_id="doc-9",
            text="persisted",
            embedding=[0.0, 1.0, 0.0],
        )
    )

    second_store = VectorStore(index_dir=index_dir, dimension=3)
    results = second_store.search([0.0, 1.0, 0.0], limit=1)

    assert (index_dir / "vectors.faiss").exists()
    assert (index_dir / "vectors.json").exists()
    assert len(second_store.records) == 1
    assert results[0][0].chunk_id == "chunk-9"
