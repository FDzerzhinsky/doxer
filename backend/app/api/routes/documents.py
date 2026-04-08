from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.core.dependencies import get_document_service, get_rag_service
from app.models.chat import AskRequest, ChatResponse
from app.models.document import (
    DocumentDetail,
    DocumentListItem,
    DocumentListResponse,
    DocumentUploadResponse,
)
from app.services.document_service import DocumentService
from app.services.rag_service import RagService


router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    document_service: DocumentService = Depends(get_document_service),
) -> DocumentUploadResponse:
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Filename is required.")

    record = await document_service.register_upload(file)
    return DocumentUploadResponse.model_validate(record)


@router.get("", response_model=DocumentListResponse)
def list_documents(
    document_service: DocumentService = Depends(get_document_service),
) -> DocumentListResponse:
    documents = [DocumentListItem.model_validate(document) for document in document_service.list_documents()]
    return DocumentListResponse(documents=documents)


@router.get("/{document_id}", response_model=DocumentDetail)
def get_document(
    document_id: str,
    document_service: DocumentService = Depends(get_document_service),
) -> DocumentDetail:
    document = document_service.get_document(document_id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")
    return DocumentDetail.model_validate(document)
