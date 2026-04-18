"""
EN: File: app/core/dependencies.py
EN: Purpose: Provides core configuration and dependency wiring utilities.
EN: Scope: Documents key classes, functions, and execution flow in two languages.
EN: Notes: Keep comments concise and aligned with implementation changes.
RU: Файл: app/core/dependencies.py
RU: Назначение: Содержит базовые настройки и привязку зависимостей.
RU: Область: Документирует ключевые классы, функции и поток выполнения на двух языках.
RU: Примечание: Держите комментарии лаконичными и синхронизированными с кодом.
"""

from functools import lru_cache

from app.core.config import Settings, get_settings
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.rag_service import RagService
from app.repositories.metadata_store import JsonMetadataStore
from app.services.vector_store import VectorStore


# EN: Function get_vector_store executes a specific reusable operation.
# RU: Функция get_vector_store выполняет конкретную переиспользуемую операцию.
@lru_cache(maxsize=1)
def get_vector_store() -> VectorStore:
    settings = get_settings()
    embedding_service = get_embedding_service()
    return VectorStore(
        index_dir=settings.index_path,
        dimension=embedding_service.dimension,
        embedding_signature=embedding_service.signature,
        reembed_texts=embedding_service.embed_passages,
    )


# EN: Function get_embedding_service executes a specific reusable operation.
# RU: Функция get_embedding_service выполняет конкретную переиспользуемую операцию.
@lru_cache(maxsize=1)
def get_embedding_service() -> EmbeddingService:
    settings = get_settings()
    return EmbeddingService(
        provider=settings.embedding_provider,
        model_name=settings.embedding_model,
        query_prefix=settings.embedding_query_prefix,
        passage_prefix=settings.embedding_passage_prefix,
        batch_size=settings.embedding_batch_size,
    )


# EN: Function get_llm_service executes a specific reusable operation.
# RU: Функция get_llm_service выполняет конкретную переиспользуемую операцию.
@lru_cache(maxsize=1)
def get_llm_service() -> LLMService:
    return LLMService()


# EN: Function get_metadata_store executes a specific reusable operation.
# RU: Функция get_metadata_store выполняет конкретную переиспользуемую операцию.
@lru_cache(maxsize=1)
def get_metadata_store() -> JsonMetadataStore:
    settings = get_settings()
    return JsonMetadataStore(settings.metadata_dir)


# EN: Function get_document_service executes a specific reusable operation.
# RU: Функция get_document_service выполняет конкретную переиспользуемую операцию.
@lru_cache(maxsize=1)
def get_document_service() -> DocumentService:
    settings = get_settings()
    return DocumentService(
        settings=settings,
        embedding_service=get_embedding_service(),
        vector_store=get_vector_store(),
        metadata_store=get_metadata_store(),
    )


# EN: Function get_rag_service executes a specific reusable operation.
# RU: Функция get_rag_service выполняет конкретную переиспользуемую операцию.
@lru_cache(maxsize=1)
def get_rag_service() -> RagService:
    settings = get_settings()
    return RagService(
        settings=settings,
        document_service=get_document_service(),
        embedding_service=get_embedding_service(),
        vector_store=get_vector_store(),
        llm_service=get_llm_service(),
    )
