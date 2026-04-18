"""Embedding providers for retrieval vectors."""

from __future__ import annotations

from hashlib import sha256
from typing import Any

import numpy as np


class EmbeddingServiceError(RuntimeError):
    pass


class EmbeddingService:
    def __init__(
        self,
        provider: str = "sentence-transformers",
        model_name: str = "intfloat/multilingual-e5-base",
        query_prefix: str = "query: ",
        passage_prefix: str = "passage: ",
        batch_size: int = 32,
        dimension: int | None = None,
    ) -> None:
        self.provider = provider.strip().lower()
        self.model_name = model_name
        self.query_prefix = query_prefix
        self.passage_prefix = passage_prefix
        self.batch_size = batch_size
        self._model: Any | None = None

        if dimension is not None:
            self._dimension = dimension
        elif self.provider == "hash":
            self._dimension = 8
        else:
            self._dimension = None

    @property
    def dimension(self) -> int:
        if self._dimension is not None:
            return self._dimension

        if self.provider == "sentence-transformers":
            model = self._get_sentence_transformer_model()
            self._dimension = int(model.get_sentence_embedding_dimension())
            return self._dimension

        raise EmbeddingServiceError(f"Unsupported embedding provider: {self.provider}")

    @property
    def signature(self) -> str:
        return f"{self.provider}:{self.model_name}:q={self.query_prefix}:p={self.passage_prefix}"

    def embed_query(self, text: str) -> list[float]:
        if self.provider == "sentence-transformers":
            formatted = self._apply_prefix(self.query_prefix, text)
            vectors = self._encode_with_sentence_transformers([formatted])
            self._validate_vectors(vectors)
            return vectors[0].tolist()

        if self.provider == "hash":
            return self._hash_embed(self._apply_prefix(self.query_prefix, text))

        raise EmbeddingServiceError(f"Unsupported embedding provider: {self.provider}")

    def embed_passages(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        if self.provider == "sentence-transformers":
            formatted = [self._apply_prefix(self.passage_prefix, text) for text in texts]
            vectors = self._encode_with_sentence_transformers(formatted)
            self._validate_vectors(vectors)
            return vectors.tolist()

        if self.provider == "hash":
            return [self._hash_embed(self._apply_prefix(self.passage_prefix, text)) for text in texts]

        raise EmbeddingServiceError(f"Unsupported embedding provider: {self.provider}")

    def embed_text(self, text: str) -> list[float]:
        return self.embed_query(text)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return self.embed_passages(texts)

    def _apply_prefix(self, prefix: str, text: str) -> str:
        if not prefix:
            return text
        if text.startswith(prefix):
            return text
        return f"{prefix}{text}"

    def _hash_embed(self, text: str) -> list[float]:
        target_dimension = self.dimension
        digest = sha256(text.encode("utf-8")).digest()
        values: list[float] = []
        current = digest
        while len(values) < target_dimension:
            values.extend(byte / 255.0 for byte in current)
            current = sha256(current).digest()
        return values[:target_dimension]

    def _get_sentence_transformer_model(self) -> Any:
        if self._model is not None:
            return self._model

        try:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self.model_name)
            return self._model
        except Exception as exc:  # pragma: no cover - runtime environment guard
            raise EmbeddingServiceError(
                "Failed to initialize sentence-transformers model. "
                "Install dependencies and ensure the model can be downloaded or is cached."
            ) from exc

    def _encode_with_sentence_transformers(self, texts: list[str]) -> np.ndarray:
        model = self._get_sentence_transformer_model()
        vectors = model.encode(
            texts,
            batch_size=self.batch_size,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        vectors_np = np.asarray(vectors, dtype="float32")
        if vectors_np.ndim == 1:
            vectors_np = vectors_np.reshape(1, -1)
        return vectors_np

    def _validate_vectors(self, vectors: np.ndarray) -> None:
        if vectors.ndim != 2:
            raise EmbeddingServiceError(f"Expected 2D embedding array, got shape {vectors.shape}")
        if vectors.shape[1] != self.dimension:
            raise EmbeddingServiceError(
                f"Embedding dimension mismatch. Expected {self.dimension}, got {vectors.shape[1]}."
            )
