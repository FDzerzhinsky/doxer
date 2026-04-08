from __future__ import annotations


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size - 1.")

    stripped_text = text.strip()
    if not stripped_text:
        return []

    chunks: list[str] = []
    start = 0
    while start < len(stripped_text):
        end = min(len(stripped_text), start + chunk_size)
        chunks.append(stripped_text[start:end])
        if end == len(stripped_text):
            break
        start = end - overlap

    return chunks
