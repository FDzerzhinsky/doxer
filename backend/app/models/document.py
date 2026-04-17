"""
EN: File: app/models/document.py
EN: Purpose: Declares data models used across the application layers.
EN: Scope: Documents key classes, functions, and execution flow in two languages.
EN: Notes: Keep comments concise and aligned with implementation changes.
RU: Файл: app/models/document.py
RU: Назначение: Описывает модели данных, используемые в слоях приложения.
RU: Область: Документирует ключевые классы, функции и поток выполнения на двух языках.
RU: Примечание: Держите комментарии лаконичными и синхронизированными с кодом.
"""

from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field


# EN: Class DocumentBase groups related state and behavior.
# RU: Класс DocumentBase объединяет связанное состояние и поведение.
class DocumentBase(BaseModel):
    document_id: str
    filename: str
    status: str
    uploaded_at: datetime
    chunks_created: int = 0
    embedding_model: str | None = None


# EN: Class DocumentRecord groups related state and behavior.
# RU: Класс DocumentRecord объединяет связанное состояние и поведение.
class DocumentRecord(DocumentBase):
    content_type: str | None = None
    file_path: Path | None = None


# EN: Class DocumentChunkRecord groups related state and behavior.
# RU: Класс DocumentChunkRecord объединяет связанное состояние и поведение.
class DocumentChunkRecord(BaseModel):
    chunk_id: str
    document_id: str
    chunk_index: int
    text: str
    page: int | None = None
    character_count: int = 0


# EN: Class DocumentUploadResponse groups related state and behavior.
# RU: Класс DocumentUploadResponse объединяет связанное состояние и поведение.
class DocumentUploadResponse(DocumentBase):
    pass


# EN: Class DocumentListItem groups related state and behavior.
# RU: Класс DocumentListItem объединяет связанное состояние и поведение.
class DocumentListItem(DocumentBase):
    pass


# EN: Class DocumentListResponse groups related state and behavior.
# RU: Класс DocumentListResponse объединяет связанное состояние и поведение.
class DocumentListResponse(BaseModel):
    documents: list[DocumentListItem]


# EN: Class DocumentDetail groups related state and behavior.
# RU: Класс DocumentDetail объединяет связанное состояние и поведение.
class DocumentDetail(DocumentRecord):
    pass
