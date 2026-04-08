from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field


class DocumentBase(BaseModel):
    document_id: str
    filename: str
    status: str
    uploaded_at: datetime
    chunks_created: int = 0
    embedding_model: str | None = None


class DocumentRecord(DocumentBase):
    content_type: str | None = None
    file_path: Path | None = None


class DocumentUploadResponse(DocumentBase):
    pass


class DocumentListItem(DocumentBase):
    pass


class DocumentListResponse(BaseModel):
    documents: list[DocumentListItem]


class DocumentDetail(DocumentRecord):
    pass
