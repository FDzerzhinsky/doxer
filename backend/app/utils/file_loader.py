"""
EN: File: app/utils/file_loader.py
EN: Purpose: Provides reusable utility helpers for common operations.
EN: Scope: Documents key classes, functions, and execution flow in two languages.
EN: Notes: Keep comments concise and aligned with implementation changes.
RU: Файл: app/utils/file_loader.py
RU: Назначение: Содержит переиспользуемые утилиты для типовых операций.
RU: Область: Документирует ключевые классы, функции и поток выполнения на двух языках.
RU: Примечание: Держите комментарии лаконичными и синхронизированными с кодом.
"""

from __future__ import annotations

from pathlib import Path


# EN: Function load_document_text executes a specific reusable operation.
# RU: Функция load_document_text выполняет конкретную переиспользуемую операцию.
def load_document_text(file_path: Path) -> str:
    suffix = file_path.suffix.lower()
    if suffix in {".txt", ".md"}:
        return file_path.read_text(encoding="utf-8")

    if suffix == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise RuntimeError("PDF support requires the 'pypdf' package.") from exc

        reader = PdfReader(str(file_path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    raise ValueError(f"Unsupported file type: {suffix}")
