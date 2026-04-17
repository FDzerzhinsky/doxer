"""
EN: File: app/scripts/stdio.py
EN: Purpose: Provides command-line or helper script entry points.
EN: Scope: Documents key classes, functions, and execution flow in two languages.
EN: Notes: Keep comments concise and aligned with implementation changes.
RU: Файл: app/scripts/stdio.py
RU: Назначение: Предоставляет CLI-точки входа и вспомогательные скрипты.
RU: Область: Документирует ключевые классы, функции и поток выполнения на двух языках.
RU: Примечание: Держите комментарии лаконичными и синхронизированными с кодом.
"""

from __future__ import annotations

import sys


# EN: Function configure_utf8_stdio executes a specific reusable operation.
# RU: Функция configure_utf8_stdio выполняет конкретную переиспользуемую операцию.
def configure_utf8_stdio() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
