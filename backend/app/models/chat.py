from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(min_length=1)
    document_id: str = Field(min_length=1)


class SourceChunk(BaseModel):
    chunk_id: str
    page: int | None = None
    score: float
    text: str | None = None


class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceChunk] = Field(default_factory=list)
