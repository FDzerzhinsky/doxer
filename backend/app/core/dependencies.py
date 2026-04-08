from functools import lru_cache

from app.core.config import Settings, get_settings
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.rag_service import RagService
from app.services.vector_store import VectorStore


@lru_cache(maxsize=1)
def get_vector_store() -> VectorStore:
    return VectorStore()


@lru_cache(maxsize=1)
def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()


@lru_cache(maxsize=1)
def get_llm_service() -> LLMService:
    return LLMService()


@lru_cache(maxsize=1)
def get_document_service() -> DocumentService:
    settings = get_settings()
    return DocumentService(
        settings=settings,
        embedding_service=get_embedding_service(),
        vector_store=get_vector_store(),
    )


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
