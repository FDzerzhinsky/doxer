from __future__ import annotations

from hashlib import sha256


class EmbeddingService:
    def __init__(self, dimension: int = 8) -> None:
        self.dimension = dimension

    def embed_text(self, text: str) -> list[float]:
        digest = sha256(text.encode("utf-8")).digest()
        values = [digest[index] / 255.0 for index in range(self.dimension)]
        return values

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_text(text) for text in texts]
