"""
EN: File: tests/test_file_loader.py
EN: Purpose: Contains automated tests validating application behavior and edge cases.
EN: Scope: Documents key classes, functions, and execution flow in two languages.
EN: Notes: Keep comments concise and aligned with implementation changes.
RU: Файл: tests/test_file_loader.py
RU: Назначение: Содержит автотесты, проверяющие поведение приложения и граничные случаи.
RU: Область: Документирует ключевые классы, функции и поток выполнения на двух языках.
RU: Примечание: Держите комментарии лаконичными и синхронизированными с кодом.
"""

from pathlib import Path

import pytest

from app.utils.file_loader import load_document_text


# EN: Function test_load_document_text_reads_plain_text executes a specific reusable operation.
# RU: Функция test_load_document_text_reads_plain_text выполняет конкретную переиспользуемую операцию.
def test_load_document_text_reads_plain_text(tmp_path: Path) -> None:
    file_path = tmp_path / "note.txt"
    file_path.write_text("hello backend", encoding="utf-8")

    assert load_document_text(file_path) == "hello backend"


# EN: Function test_load_document_text_rejects_unsupported_file executes a specific reusable operation.
# RU: Функция test_load_document_text_rejects_unsupported_file выполняет конкретную переиспользуемую операцию.
def test_load_document_text_rejects_unsupported_file(tmp_path: Path) -> None:
    file_path = tmp_path / "note.csv"
    file_path.write_text("a,b,c", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported file type"):
        load_document_text(file_path)
