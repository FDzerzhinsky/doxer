"""
EN: File: app/models/chat.py
EN: Purpose: Declares data models used across the application layers.
EN: Scope: Documents key classes, functions, and execution flow in two languages.
EN: Notes: Keep comments concise and aligned with implementation changes.
RU: Файл: app/models/chat.py
RU: Назначение: Описывает модели данных, используемые в слоях приложения.
RU: Область: Документирует ключевые классы, функции и поток выполнения на двух языках.
RU: Примечание: Держите комментарии лаконичными и синхронизированными с кодом.
"""

from pydantic import BaseModel, Field


# EN: Class AskRequest groups related state and behavior.
# RU: Класс AskRequest объединяет связанное состояние и поведение.
class AskRequest(BaseModel):
    question: str = Field(min_length=1)
    document_id: str = Field(min_length=1)


# EN: Class SourceChunk groups related state and behavior.
# RU: Класс SourceChunk объединяет связанное состояние и поведение.
class SourceChunk(BaseModel):
    chunk_id: str
    page: int | None = None
    score: float
    text: str | None = None


# EN: Class ChatResponse groups related state and behavior.
# RU: Класс ChatResponse объединяет связанное состояние и поведение.
class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceChunk] = Field(default_factory=list)
