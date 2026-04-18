"""
EN: File: app/scripts/ask_document.py
EN: Purpose: Provides command-line or helper script entry points.
EN: Scope: Documents key classes, functions, and execution flow in two languages.
EN: Notes: Keep comments concise and aligned with implementation changes.
RU: Файл: app/scripts/ask_document.py
RU: Назначение: Предоставляет CLI-точки входа и вспомогательные скрипты.
RU: Область: Документирует ключевые классы, функции и поток выполнения на двух языках.
RU: Примечание: Держите комментарии лаконичными и синхронизированными с кодом.
"""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from app.core.config import Settings
from app.models.chat import AskRequest
from app.repositories.metadata_store import JsonMetadataStore
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.rag_service import RagService
from app.services.vector_store import VectorStore
from app.scripts.stdio import configure_utf8_stdio


# EN: Function build_parser executes a specific reusable operation.
# RU: Функция build_parser выполняет конкретную переиспользуемую операцию.
def build_parser(default_llm_provider: str | None = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ingest a local document and ask a question against it.")
    parser.add_argument("file", nargs="?", help="Path to a local TXT, MD, or PDF file")
    parser.add_argument("--file", dest="file_path", help="Path to a local TXT, MD, or PDF file")
    parser.add_argument("--question", required=True, help="Question to ask about the document")
    parser.add_argument("--workspace-dir", help="Optional directory for uploads, index, and metadata output")
    parser.add_argument("--chunk-size", type=int, default=1000, help="Chunk size in characters")
    parser.add_argument("--chunk-overlap", type=int, default=200, help="Chunk overlap in characters")
    parser.add_argument(
        "--llm-provider",
        choices=["mock", "ollama"],
        default=default_llm_provider,
        help="Override the LLM provider for this run",
    )
    parser.add_argument("--ollama-base-url", help="Override the Ollama base URL for this run")
    parser.add_argument("--ollama-model", help="Override the Ollama model for this run")
    parser.add_argument("--llm-temperature", type=float, help="Override the LLM temperature for this run")
    parser.add_argument("--llm-timeout", type=float, help="Override the LLM timeout for this run")
    return parser


# EN: Function build_settings executes a specific reusable operation.
# RU: Функция build_settings выполняет конкретную переиспользуемую операцию.
def build_settings(
    workspace_dir: Path | None,
    chunk_size: int,
    chunk_overlap: int,
    llm_provider: str | None = None,
    ollama_base_url: str | None = None,
    ollama_model: str | None = None,
    llm_temperature: float | None = None,
    llm_timeout: float | None = None,
) -> tuple[Settings, Path]:
    if workspace_dir is None:
        workspace_dir = Path(tempfile.mkdtemp(prefix="doxer-chat-"))
    else:
        workspace_dir.mkdir(parents=True, exist_ok=True)

    settings_kwargs: dict[str, object] = {
        "upload_dir": workspace_dir / "uploads",
        "index_path": workspace_dir / "index",
        "metadata_dir": workspace_dir / "metadata",
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
    }
    if llm_provider is not None:
        settings_kwargs["llm_provider"] = llm_provider
    if ollama_base_url is not None:
        settings_kwargs["ollama_base_url"] = ollama_base_url
    if ollama_model is not None:
        settings_kwargs["ollama_model"] = ollama_model
    if llm_temperature is not None:
        settings_kwargs["llm_temperature"] = llm_temperature
    if llm_timeout is not None:
        settings_kwargs["llm_timeout"] = llm_timeout

    settings = Settings(**settings_kwargs)
    return settings, workspace_dir


# EN: Function main executes a specific reusable operation.
# RU: Функция main выполняет конкретную переиспользуемую операцию.
def main(default_llm_provider: str | None = None) -> int:
    configure_utf8_stdio()
    parser = build_parser(default_llm_provider=default_llm_provider)
    args = parser.parse_args()

    source_file_arg = args.file_path or args.file
    if not source_file_arg:
        parser.error("the file path is required, use FILE or --file FILE")

    source_file = Path(source_file_arg).expanduser().resolve()
    if not source_file.exists():
        raise SystemExit(f"File not found: {source_file}")

    workspace_dir_arg = Path(args.workspace_dir).expanduser().resolve() if args.workspace_dir else None
    settings, workspace_dir = build_settings(
        workspace_dir_arg,
        args.chunk_size,
        args.chunk_overlap,
        llm_provider=args.llm_provider,
        ollama_base_url=args.ollama_base_url,
        ollama_model=args.ollama_model,
        llm_temperature=args.llm_temperature,
        llm_timeout=args.llm_timeout,
    )
    embedding_service = EmbeddingService(
        provider=settings.embedding_provider,
        model_name=settings.embedding_model,
        query_prefix=settings.embedding_query_prefix,
        passage_prefix=settings.embedding_passage_prefix,
        batch_size=settings.embedding_batch_size,
    )
    vector_store = VectorStore(
        index_dir=settings.index_path,
        dimension=embedding_service.dimension,
        embedding_signature=embedding_service.signature,
        reembed_texts=embedding_service.embed_passages,
    )
    metadata_store = JsonMetadataStore(settings.metadata_dir)
    document_service = DocumentService(
        settings=settings,
        embedding_service=embedding_service,
        vector_store=vector_store,
        metadata_store=metadata_store,
    )
    rag_service = RagService(
        settings=settings,
        document_service=document_service,
        embedding_service=embedding_service,
        vector_store=vector_store,
        llm_service=LLMService(settings=settings),
    )

    try:
        record = document_service.register_local_file(source_file)
        response = rag_service.answer_question(
            AskRequest(question=args.question, document_id=record.document_id)
        )
        snapshot = document_service.build_document_snapshot(record.document_id)
    except Exception as exc:  # pragma: no cover - CLI guard
        raise SystemExit(f"Failed to ask question for {source_file}: {exc}") from exc

    payload = {
        "source_file": str(source_file),
        "workspace_dir": str(workspace_dir),
        "question": response.question,
        "answer": response.answer,
        "sources": [source.model_dump(mode="json") for source in response.sources],
        **snapshot,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entrypoint
    raise SystemExit(main())
