from __future__ import annotations

import json
import os
import subprocess
import sys


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
        env={**os.environ},
    )

    payload = json.loads(completed.stdout)

    assert payload["question"] == "What is the remote work policy?"
    assert payload["answer"]
    assert payload["sources"]
    assert payload["document"]["filename"] == "policy.txt"
    assert payload["vector_count"] == payload["document"]["chunks_created"]
