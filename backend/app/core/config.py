"""
EN: File: app/core/config.py
EN: Purpose: Provides core configuration and dependency wiring utilities.
EN: Scope: Documents key classes, functions, and execution flow in two languages.
EN: Notes: Keep comments concise and aligned with implementation changes.
RU: Файл: app/core/config.py
RU: Назначение: Содержит базовые настройки и привязку зависимостей.
RU: Область: Документирует ключевые классы, функции и поток выполнения на двух языках.
RU: Примечание: Держите комментарии лаконичными и синхронизированными с кодом.
"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# EN: Class Settings groups related state and behavior.
# RU: Класс Settings объединяет связанное состояние и поведение.
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "AI Document Assistant"
    environment: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    embedding_provider: str = "sentence-transformers"
    embedding_model: str = "intfloat/multilingual-e5-base"
    embedding_query_prefix: str = "query: "
    embedding_passage_prefix: str = "passage: "
    embedding_batch_size: int = 32
    llm_provider: str = "mock"
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "qwen2.5:7b"
    ollama_keep_alive: str = "1h"
    llm_temperature: float = 0.2
    llm_timeout: float = 60.0

    vector_store: str = "faiss"
    upload_dir: Path = Field(default=Path("./data/uploads"))
    index_path: Path = Field(default=Path("./data/index"))
    metadata_dir: Path = Field(default=Path("./data/metadata"))

    chunk_size: int = 1000
    chunk_overlap: int = 200
    max_search_results: int = 5

    # EN: Method ensure_directories performs a focused step of the class workflow.
    # RU: Метод ensure_directories выполняет целевой шаг в рабочем процессе класса.
    def ensure_directories(self) -> None:
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.index_path.mkdir(parents=True, exist_ok=True)
        self.metadata_dir.mkdir(parents=True, exist_ok=True)


# EN: Function get_settings executes a specific reusable operation.
# RU: Функция get_settings выполняет конкретную переиспользуемую операцию.
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    settings = Settings()
    settings.ensure_directories()
    return settings
