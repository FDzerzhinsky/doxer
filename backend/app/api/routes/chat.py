from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_rag_service
from app.models.chat import AskRequest, ChatResponse
from app.services.rag_service import RagService


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/ask", response_model=ChatResponse)
def ask_question(
    payload: AskRequest,
    rag_service: RagService = Depends(get_rag_service),
) -> ChatResponse:
    if not payload.document_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="document_id is required.")
    return rag_service.answer_question(payload)
