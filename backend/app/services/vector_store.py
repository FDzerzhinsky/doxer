from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from threading import RLock

import faiss
import numpy as np


@dataclass
class VectorRecord:
    chunk_id: str
    document_id: str
    text: str
    embedding: list[float]
    page: int | None = None


class VectorStore:
    def __init__(self, index_dir: Path | None = None, dimension: int = 8) -> None:
        self.index_dir = Path(index_dir or Path("./data/index"))
        self.dimension = dimension
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.index_dir / "vectors.faiss"
        self.records_file = self.index_dir / "vectors.json"
        self._lock = RLock()
        self.records: list[VectorRecord] = self._load_records()
        self._index = self._create_index()
        self._rebuild_index()

    def upsert(self, record: VectorRecord) -> None:
        with self._lock:
            vector = self._normalize_vector(record.embedding)
            vector_id = len(self.records)
            self.records.append(record)
            self._add_vector(vector_id, vector)
            self._persist_state()

    def search(self, query_embedding: list[float], document_id: str | None = None, limit: int = 5) -> list[tuple[VectorRecord, float]]:
        with self._lock:
            if limit <= 0 or not self.records:
                return []

            query = self._normalize_vector(query_embedding)
            scores, ids = self._index.search(query, len(self.records))

            results: list[tuple[VectorRecord, float]] = []
            for vector_id, score in zip(ids[0], scores[0], strict=False):
                if vector_id < 0:
                    continue

                record = self.records[int(vector_id)]
                if document_id is not None and record.document_id != document_id:
                    continue

                results.append((record, float(score)))
                if len(results) >= limit:
                    break

            return results

    def _create_index(self) -> faiss.IndexIDMap2:
        return faiss.IndexIDMap2(faiss.IndexFlatIP(self.dimension))

    def _rebuild_index(self) -> None:
        self._index = self._create_index()
        if not self.records:
            self._persist_index()
            return

        vectors = np.asarray([record.embedding for record in self.records], dtype="float32")
        self._validate_dimensions(vectors)
        faiss.normalize_L2(vectors)
        ids = np.arange(len(self.records), dtype=np.int64)
        self._index.add_with_ids(vectors, ids)
        self._persist_index()

    def _add_vector(self, vector_id: int, vector: np.ndarray) -> None:
        ids = np.asarray([vector_id], dtype=np.int64)
        self._index.add_with_ids(vector, ids)

    def _normalize_vector(self, embedding: list[float]) -> np.ndarray:
        vector = np.asarray([embedding], dtype="float32")
        self._validate_dimensions(vector)
        faiss.normalize_L2(vector)
        return vector

    def _validate_dimensions(self, vectors: np.ndarray) -> None:
        if vectors.ndim != 2 or vectors.shape[1] != self.dimension:
            raise ValueError(f"Expected embeddings with dimension {self.dimension}, got shape {vectors.shape}.")

    def _load_records(self) -> list[VectorRecord]:
        if not self.records_file.exists():
            return []

        raw_records = json.loads(self.records_file.read_text(encoding="utf-8"))
        return [VectorRecord(**payload) for payload in raw_records]

    def _persist_state(self) -> None:
        self._persist_records()
        self._persist_index()

    def _persist_records(self) -> None:
        payload = [asdict(record) for record in self.records]
        self.records_file.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")

    def _persist_index(self) -> None:
        faiss.write_index(self._index, str(self.index_file))
