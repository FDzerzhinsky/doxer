"""
EN: File: app/scripts/inspect_ingestion.py
EN: Purpose: Provides command-line or helper script entry points.
EN: Scope: Documents key classes, functions, and execution flow in two languages.
EN: Notes: Keep comments concise and aligned with implementation changes.
RU: Файл: app/scripts/inspect_ingestion.py
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
from app.repositories.metadata_store import JsonMetadataStore
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.scripts.stdio import configure_utf8_stdio


# EN: Function build_parser executes a specific reusable operation.
# RU: Функция build_parser выполняет конкретную переиспользуемую операцию.
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect document ingestion and print chunks plus metadata as JSON.")
    parser.add_argument("file", nargs="?", help="Path to a local TXT, MD, or PDF file")
    parser.add_argument("--file", dest="file_path", help="Path to a local TXT, MD, or PDF file")
    parser.add_argument("--workspace-dir", help="Optional directory for uploads, index, and metadata output")
    parser.add_argument("--chunk-size", type=int, default=1000, help="Chunk size in characters")
    parser.add_argument("--chunk-overlap", type=int, default=200, help="Chunk overlap in characters")
    return parser


# EN: Function build_settings executes a specific reusable operation.
# RU: Функция build_settings выполняет конкретную переиспользуемую операцию.
def build_settings(workspace_dir: Path | None, chunk_size: int, chunk_overlap: int) -> tuple[Settings, Path]:
    if workspace_dir is None:
        workspace_dir = Path(tempfile.mkdtemp(prefix="doxer-ingestion-"))
    else:
        workspace_dir.mkdir(parents=True, exist_ok=True)

    settings = Settings(
        upload_dir=workspace_dir / "uploads",
        index_path=workspace_dir / "index",
        metadata_dir=workspace_dir / "metadata",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return settings, workspace_dir


# EN: Function main executes a specific reusable operation.
# RU: Функция main выполняет конкретную переиспользуемую операцию.
def main() -> int:
    configure_utf8_stdio()
    parser = build_parser()
    args = parser.parse_args()

    source_file_arg = args.file_path or args.file
    if not source_file_arg:
        parser.error("the file path is required, use FILE or --file FILE")

    source_file = Path(source_file_arg).expanduser().resolve()
    if not source_file.exists():
        raise SystemExit(f"File not found: {source_file}")

    workspace_dir_arg = Path(args.workspace_dir).expanduser().resolve() if args.workspace_dir else None
    settings, workspace_dir = build_settings(workspace_dir_arg, args.chunk_size, args.chunk_overlap)
    embedding_service = EmbeddingService()

    document_service = DocumentService(
        settings=settings,
        embedding_service=embedding_service,
        vector_store=VectorStore(index_dir=settings.index_path, dimension=embedding_service.dimension),
        metadata_store=JsonMetadataStore(settings.metadata_dir),
    )

    try:
        record = document_service.register_local_file(source_file)
        snapshot = document_service.build_document_snapshot(record.document_id)
    except Exception as exc:  # pragma: no cover - CLI guard
        raise SystemExit(f"Failed to inspect ingestion for {source_file}: {exc}") from exc

    payload = {
        "source_file": str(source_file),
        "workspace_dir": str(workspace_dir),
        **snapshot,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entrypoint
    raise SystemExit(main())
