from __future__ import annotations

from app.scripts.ask_document import main as ask_document_main


def main() -> int:
    return ask_document_main(default_llm_provider="ollama")


if __name__ == "__main__":  # pragma: no cover - CLI entrypoint
    raise SystemExit(main())
