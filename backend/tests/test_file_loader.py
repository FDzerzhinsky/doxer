from pathlib import Path

import pytest

from app.utils.file_loader import load_document_text


def test_load_document_text_reads_plain_text(tmp_path: Path) -> None:
    file_path = tmp_path / "note.txt"
    file_path.write_text("hello backend", encoding="utf-8")

    assert load_document_text(file_path) == "hello backend"


def test_load_document_text_rejects_unsupported_file(tmp_path: Path) -> None:
    file_path = tmp_path / "note.csv"
    file_path.write_text("a,b,c", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported file type"):
        load_document_text(file_path)
