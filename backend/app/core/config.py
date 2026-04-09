from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "AI Document Assistant"
    environment: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    llm_provider: str = "mock"
    ollama_model: str = "llama3.1"

    vector_store: str = "faiss"
    upload_dir: Path = Field(default=Path("./data/uploads"))
    index_path: Path = Field(default=Path("./data/index"))
    metadata_dir: Path = Field(default=Path("./data/metadata"))

    chunk_size: int = 1000
    chunk_overlap: int = 200
    max_search_results: int = 5

    def ensure_directories(self) -> None:
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.index_path.mkdir(parents=True, exist_ok=True)
        self.metadata_dir.mkdir(parents=True, exist_ok=True)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    settings = Settings()
    settings.ensure_directories()
    return settings
