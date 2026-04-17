"""
EN: File: app/api/routes/chat.py
EN: Purpose: Defines API endpoint handlers for a specific route group.
EN: Scope: Documents key classes, functions, and execution flow in two languages.
EN: Notes: Keep comments concise and aligned with implementation changes.
RU: Файл: app/api/routes/chat.py
RU: Назначение: Определяет обработчики API-эндпоинтов для конкретной группы маршрутов.
RU: Область: Документирует ключевые классы, функции и поток выполнения на двух языках.
RU: Примечание: Держите комментарии лаконичными и синхронизированными с кодом.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_rag_service
from app.models.chat import AskRequest, ChatResponse
from app.services.rag_service import RagService


router = APIRouter(prefix="/chat", tags=["chat"])


# EN: Function ask_question executes a specific reusable operation.
# RU: Функция ask_question выполняет конкретную переиспользуемую операцию.
@router.post("/ask", response_model=ChatResponse)
def ask_question(
    payload: AskRequest,
    rag_service: RagService = Depends(get_rag_service),
) -> ChatResponse:
    if not payload.document_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="document_id is required.")
    return rag_service.answer_question(payload)
