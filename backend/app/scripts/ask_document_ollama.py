"""
EN: File: app/scripts/ask_document_ollama.py
EN: Purpose: Provides command-line or helper script entry points.
EN: Scope: Documents key classes, functions, and execution flow in two languages.
EN: Notes: Keep comments concise and aligned with implementation changes.
RU: Файл: app/scripts/ask_document_ollama.py
RU: Назначение: Предоставляет CLI-точки входа и вспомогательные скрипты.
RU: Область: Документирует ключевые классы, функции и поток выполнения на двух языках.
RU: Примечание: Держите комментарии лаконичными и синхронизированными с кодом.
"""

from __future__ import annotations

from app.scripts.ask_document import main as ask_document_main


# EN: Function main executes a specific reusable operation.
# RU: Функция main выполняет конкретную переиспользуемую операцию.
def main() -> int:
    return ask_document_main(default_llm_provider="ollama")


if __name__ == "__main__":  # pragma: no cover - CLI entrypoint
    raise SystemExit(main())
