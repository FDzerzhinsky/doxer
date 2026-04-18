from __future__ import annotations

import numpy as np

from app.services.embedding_service import EmbeddingService


def test_hash_embeddings_are_deterministic() -> None:
    service = EmbeddingService(
        provider="hash",
        model_name="hash-test-model",
        query_prefix="",
        passage_prefix="",
        dimension=8,
    )

    first = service.embed_query("same text")
    second = service.embed_query("same text")

    assert first == second
    assert len(first) == 8


def test_sentence_transformer_embedding_uses_query_and_passage_prefixes(monkeypatch) -> None:
    captured_inputs: list[str] = []

    def fake_encoder(self: EmbeddingService, texts: list[str]) -> np.ndarray:
        captured_inputs.extend(texts)
        return np.asarray([[1.0, 0.0, 0.0] for _ in texts], dtype="float32")

    monkeypatch.setattr(EmbeddingService, "_encode_with_sentence_transformers", fake_encoder)

    service = EmbeddingService(
        provider="sentence-transformers",
        model_name="fake-model",
        query_prefix="query: ",
        passage_prefix="passage: ",
        dimension=3,
    )

    _ = service.embed_query("what is policy")
    _ = service.embed_query("query: already-formatted")
    _ = service.embed_passages(["chunk one", "passage: already-formatted"])

    assert captured_inputs == [
        "query: what is policy",
        "query: already-formatted",
        "passage: chunk one",
        "passage: already-formatted",
    ]
