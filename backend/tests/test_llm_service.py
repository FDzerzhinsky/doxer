from __future__ import annotations

from app.core.config import Settings
from app.services.llm_service import LLMService


def test_mock_llm_service_uses_context() -> None:
    service = LLMService(
        Settings(
            llm_provider="mock",
        )
    )

    answer = service.compose_answer("What is the policy?", "Employees may work remotely two days per week.")

    assert "mock RAG response" in answer
    assert "What is the policy?" in answer
    assert "Employees may work remotely two days per week." in answer


def test_ollama_llm_service_posts_expected_payload(monkeypatch) -> None:
    captured: dict[str, object] = {}

    class FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return {"message": {"content": "Use only the provided context."}}

    class FakeClient:
        def __init__(self, *, trust_env: bool, timeout: float) -> None:
            captured["trust_env"] = trust_env
            captured["timeout"] = timeout

        def __enter__(self) -> "FakeClient":
            return self

        def __exit__(self, exc_type, exc_value, traceback) -> None:
            return None

        def post(self, url: str, *, json: dict[str, object]) -> FakeResponse:
            captured["url"] = url
            captured["json"] = json
            return FakeResponse()

    monkeypatch.setattr("app.services.llm_service.httpx.Client", FakeClient)

    service = LLMService(
        Settings(
            llm_provider="ollama",
            ollama_base_url="http://127.0.0.1:11434",
            ollama_model="llama3.1",
            llm_temperature=0.15,
            llm_timeout=12.5,
        )
    )

    answer = service.compose_answer("What is the remote work policy?", "Employees may work remotely two days per week.")

    assert answer == "Use only the provided context."
    assert captured["url"] == "http://127.0.0.1:11434/api/chat"
    payload = captured["json"]
    assert isinstance(payload, dict)
    assert payload["model"] == "llama3.1"
    assert payload["stream"] is False
    assert payload["keep_alive"] == "1h"
    assert payload["options"] == {"temperature": 0.15}
    assert payload["messages"][0]["role"] == "system"
    assert payload["messages"][1]["role"] == "user"
    assert captured["trust_env"] is False
    assert captured["timeout"] == 12.5
