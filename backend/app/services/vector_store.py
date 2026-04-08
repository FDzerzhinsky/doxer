from __future__ import annotations

from dataclasses import dataclass, field
from math import sqrt


@dataclass
class VectorRecord:
    chunk_id: str
    document_id: str
    text: str
    embedding: list[float]
    page: int | None = None


@dataclass
class VectorStore:
    records: list[VectorRecord] = field(default_factory=list)

    def upsert(self, record: VectorRecord) -> None:
        self.records.append(record)

    def search(self, query_embedding: list[float], document_id: str | None = None, limit: int = 5) -> list[tuple[VectorRecord, float]]:
        candidates = self.records
        if document_id is not None:
            candidates = [record for record in candidates if record.document_id == document_id]

        scored = [(record, self._cosine_similarity(query_embedding, record.embedding)) for record in candidates]
        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:limit]

    @staticmethod
    def _cosine_similarity(left: list[float], right: list[float]) -> float:
        denominator = sqrt(sum(value * value for value in left)) * sqrt(sum(value * value for value in right))
        if denominator == 0:
            return 0.0
        return sum(left_value * right_value for left_value, right_value in zip(left, right)) / denominator
