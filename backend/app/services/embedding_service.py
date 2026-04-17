"""
EN: File: app/services/embedding_service.py
EN: Purpose: Implements business services used by API and scripts.
EN: Scope: Documents key classes, functions, and execution flow in two languages.
EN: Notes: Keep comments concise and aligned with implementation changes.
RU: Файл: app/services/embedding_service.py
RU: Назначение: Реализует бизнес-сервисы для API и скриптов.
RU: Область: Документирует ключевые классы, функции и поток выполнения на двух языках.
RU: Примечание: Держите комментарии лаконичными и синхронизированными с кодом.
"""

from __future__ import annotations

from hashlib import sha256


# EN: Class EmbeddingService groups related state and behavior.
# RU: Класс EmbeddingService объединяет связанное состояние и поведение.
class EmbeddingService:
    # EN: Method __init__ performs a focused step of the class workflow.
    # RU: Метод __init__ выполняет целевой шаг в рабочем процессе класса.
    def __init__(self, dimension: int = 8) -> None:
        self.dimension = dimension

    # EN: Method embed_text performs a focused step of the class workflow.
    # RU: Метод embed_text выполняет целевой шаг в рабочем процессе класса.
    def embed_text(self, text: str) -> list[float]:
        digest = sha256(text.encode("utf-8")).digest()
        values = [digest[index] / 255.0 for index in range(self.dimension)]
        return values

    # EN: Method embed_texts performs a focused step of the class workflow.
    # RU: Метод embed_texts выполняет целевой шаг в рабочем процессе класса.
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_text(text) for text in texts]
