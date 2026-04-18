"""
EN: File: app/services/rag_service.py
EN: Purpose: Implements business services used by API and scripts.
EN: Scope: Documents key classes, functions, and execution flow in two languages.
EN: Notes: Keep comments concise and aligned with implementation changes.
RU: Файл: app/services/rag_service.py
RU: Назначение: Реализует бизнес-сервисы для API и скриптов.
RU: Область: Документирует ключевые классы, функции и поток выполнения на двух языках.
RU: Примечание: Держите комментарии лаконичными и синхронизированными с кодом.
"""

from __future__ import annotations

from app.core.config import Settings
from app.models.chat import AskRequest, ChatResponse, SourceChunk
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.vector_store import VectorStore


# EN: Class RagService groups related state and behavior.
# RU: Класс RagService объединяет связанное состояние и поведение.
class RagService:
    # EN: Method __init__ performs a focused step of the class workflow.
    # RU: Метод __init__ выполняет целевой шаг в рабочем процессе класса.
    def __init__(
        self,
        settings: Settings,
        document_service: DocumentService,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
        llm_service: LLMService,
    ) -> None:
        self.settings = settings
        self.document_service = document_service
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.llm_service = llm_service

    # EN: Method answer_question performs a focused step of the class workflow.
    # RU: Метод answer_question выполняет целевой шаг в рабочем процессе класса.
    def answer_question(self, payload: AskRequest) -> ChatResponse:
        document = self.document_service.get_document(payload.document_id)
        if document is None:
            return ChatResponse(
                question=payload.question,
                answer="Document not found. Upload a file before asking questions.",
                sources=[],
            )

        query_embedding = self.embedding_service.embed_query(payload.question)
        matches = self.vector_store.search(query_embedding, document_id=payload.document_id, limit=self.settings.max_search_results)

        sources = [
            SourceChunk(
                chunk_id=record.chunk_id,
                page=record.page,
                score=score,
                text=record.text,
            )
            for record, score in matches
        ]
        context = "\n\n".join(record.text for record, _ in matches)
        answer = self.llm_service.compose_answer(payload.question, context)

        return ChatResponse(question=payload.question, answer=answer, sources=sources)
