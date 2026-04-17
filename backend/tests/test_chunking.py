"""
EN: File: tests/test_chunking.py
EN: Purpose: Contains automated tests validating application behavior and edge cases.
EN: Scope: Documents key classes, functions, and execution flow in two languages.
EN: Notes: Keep comments concise and aligned with implementation changes.
RU: Файл: tests/test_chunking.py
RU: Назначение: Содержит автотесты, проверяющие поведение приложения и граничные случаи.
RU: Область: Документирует ключевые классы, функции и поток выполнения на двух языках.
RU: Примечание: Держите комментарии лаконичными и синхронизированными с кодом.
"""

from app.utils.chunking import chunk_text


# EN: Function test_chunk_text_splits_with_overlap executes a specific reusable operation.
# RU: Функция test_chunk_text_splits_with_overlap выполняет конкретную переиспользуемую операцию.
def test_chunk_text_splits_with_overlap() -> None:
    chunks = chunk_text("abcdefghij", chunk_size=4, overlap=1)

    assert chunks == ["abcd", "defg", "ghij"]


# EN: Function test_chunk_text_rejects_invalid_overlap executes a specific reusable operation.
# RU: Функция test_chunk_text_rejects_invalid_overlap выполняет конкретную переиспользуемую операцию.
def test_chunk_text_rejects_invalid_overlap() -> None:
    try:
        chunk_text("abc", chunk_size=4, overlap=4)
    except ValueError as exc:
        assert "overlap" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
