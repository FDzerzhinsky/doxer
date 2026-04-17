"""
EN: File: tests/conftest.py
EN: Purpose: Contains automated tests validating application behavior and edge cases.
EN: Scope: Documents key classes, functions, and execution flow in two languages.
EN: Notes: Keep comments concise and aligned with implementation changes.
RU: Файл: tests/conftest.py
RU: Назначение: Содержит автотесты, проверяющие поведение приложения и граничные случаи.
RU: Область: Документирует ключевые классы, функции и поток выполнения на двух языках.
RU: Примечание: Держите комментарии лаконичными и синхронизированными с кодом.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.core.dependencies import get_document_service, get_rag_service
from app.main import app
from app.repositories.metadata_store import JsonMetadataStore
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.rag_service import RagService
from app.services.vector_store import VectorStore


# EN: Class DummyUploadFile groups related state and behavior.
# RU: Класс DummyUploadFile объединяет связанное состояние и поведение.
class DummyUploadFile:
    # EN: Method __init__ performs a focused step of the class workflow.
    # RU: Метод __init__ выполняет целевой шаг в рабочем процессе класса.
    def __init__(self, filename: str, content: bytes, content_type: str = "text/plain") -> None:
        self.filename = filename
        self.content_type = content_type
        self._content = content

    # EN: Method read performs a focused step of the class workflow.
    # RU: Метод read выполняет целевой шаг в рабочем процессе класса.
    async def read(self) -> bytes:
        return self._content


# EN: Function test_settings executes a specific reusable operation.
# RU: Функция test_settings выполняет конкретную переиспользуемую операцию.
@pytest.fixture()
def test_settings(tmp_path: Path) -> Settings:
    return Settings(
        upload_dir=tmp_path / "uploads",
        index_path=tmp_path / "index",
        metadata_dir=tmp_path / "metadata",
        chunk_size=20,
        chunk_overlap=5,
    )


# EN: Function test_services executes a specific reusable operation.
# RU: Функция test_services выполняет конкретную переиспользуемую операцию.
@pytest.fixture()
def test_services(test_settings: Settings) -> tuple[DocumentService, RagService]:
    embedding_service = EmbeddingService()
    vector_store = VectorStore(index_dir=test_settings.index_path, dimension=embedding_service.dimension)
    metadata_store = JsonMetadataStore(test_settings.metadata_dir)
    document_service = DocumentService(
        settings=test_settings,
        embedding_service=embedding_service,
        vector_store=vector_store,
        metadata_store=metadata_store,
    )
    rag_service = RagService(
        settings=test_settings,
        document_service=document_service,
        embedding_service=embedding_service,
        vector_store=vector_store,
        llm_service=LLMService(),
    )
    return document_service, rag_service


# EN: Function client executes a specific reusable operation.
# RU: Функция client выполняет конкретную переиспользуемую операцию.
@pytest.fixture()
def client(test_services: tuple[DocumentService, RagService]) -> Iterator[TestClient]:
    document_service, rag_service = test_services
    app.dependency_overrides[get_document_service] = lambda: document_service
    app.dependency_overrides[get_rag_service] = lambda: rag_service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
