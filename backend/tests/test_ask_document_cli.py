"""
EN: File: tests/test_ask_document_cli.py
EN: Purpose: Contains automated tests validating application behavior and edge cases.
EN: Scope: Documents key classes, functions, and execution flow in two languages.
EN: Notes: Keep comments concise and aligned with implementation changes.
RU: Файл: tests/test_ask_document_cli.py
RU: Назначение: Содержит автотесты, проверяющие поведение приложения и граничные случаи.
RU: Область: Документирует ключевые классы, функции и поток выполнения на двух языках.
RU: Примечание: Держите комментарии лаконичными и синхронизированными с кодом.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys


# EN: Function test_ask_document_cli_outputs_answer executes a specific reusable operation.
# RU: Функция test_ask_document_cli_outputs_answer выполняет конкретную переиспользуемую операцию.
def test_ask_document_cli_outputs_answer(tmp_path) -> None:
    source_file = tmp_path / "policy.txt"
    source_file.write_text(
        "Remote work policy: employees may work from home two days per week. The policy is reviewed quarterly.",
        encoding="utf-8",
    )

    workspace_dir = tmp_path / "workspace"
    command = [
        sys.executable,
        "-m",
        "app.scripts.ask_document",
        "--file",
        str(source_file),
        "--workspace-dir",
        str(workspace_dir),
        "--llm-provider",
        "mock",
        "--question",
        "What is the remote work policy?",
    ]

    completed = subprocess.run(
        command,
        cwd=tmp_path.parent,
        capture_output=True,
        text=True,
        check=True,
        env={
            **os.environ,
            "EMBEDDING_PROVIDER": "hash",
            "EMBEDDING_MODEL": "hash-test-model",
            "EMBEDDING_QUERY_PREFIX": "",
            "EMBEDDING_PASSAGE_PREFIX": "",
        },
    )

    payload = json.loads(completed.stdout)

    assert payload["question"] == "What is the remote work policy?"
    assert payload["answer"]
    assert payload["sources"]
    assert payload["document"]["filename"] == "policy.txt"
    assert payload["vector_count"] == payload["document"]["chunks_created"]
