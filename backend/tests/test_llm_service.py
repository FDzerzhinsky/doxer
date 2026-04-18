"""
EN: File: tests/test_llm_service.py
EN: Purpose: Contains automated tests validating application behavior and edge cases.
EN: Scope: Documents key classes, functions, and execution flow in two languages.
EN: Notes: Keep comments concise and aligned with implementation changes.
RU: Файл: tests/test_llm_service.py
RU: Назначение: Содержит автотесты, проверяющие поведение приложения и граничные случаи.
RU: Область: Документирует ключевые классы, функции и поток выполнения на двух языках.
RU: Примечание: Держите комментарии лаконичными и синхронизированными с кодом.
"""

from __future__ import annotations

from app.core.config import Settings
from app.services.llm_service import LLMService


# EN: Function test_settings_defaults_to_gpu_model executes a specific reusable operation.
# RU: Функция test_settings_defaults_to_gpu_model выполняет конкретную переиспользуемую операцию.
def test_settings_defaults_to_gpu_model() -> None:
    assert Settings().ollama_model == "qwen2.5:7b"


# EN: Function test_mock_llm_service_uses_context executes a specific reusable operation.
# RU: Функция test_mock_llm_service_uses_context выполняет конкретную переиспользуемую операцию.
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


# EN: Function test_ollama_llm_service_posts_expected_payload executes a specific reusable operation.
# RU: Функция test_ollama_llm_service_posts_expected_payload выполняет конкретную переиспользуемую операцию.
def test_ollama_llm_service_posts_expected_payload(monkeypatch) -> None:
    captured: dict[str, object] = {}

    # EN: Class FakeResponse groups related state and behavior.
    # RU: Класс FakeResponse объединяет связанное состояние и поведение.
    class FakeResponse:
        # EN: Method raise_for_status performs a focused step of the class workflow.
        # RU: Метод raise_for_status выполняет целевой шаг в рабочем процессе класса.
        def raise_for_status(self) -> None:
            return None

        # EN: Method json performs a focused step of the class workflow.
        # RU: Метод json выполняет целевой шаг в рабочем процессе класса.
        def json(self) -> dict[str, object]:
            return {"message": {"content": "Use only the provided context."}}

    # EN: Class FakeClient groups related state and behavior.
    # RU: Класс FakeClient объединяет связанное состояние и поведение.
    class FakeClient:
        # EN: Method __init__ performs a focused step of the class workflow.
        # RU: Метод __init__ выполняет целевой шаг в рабочем процессе класса.
        def __init__(self, *, trust_env: bool, timeout: float) -> None:
            captured["trust_env"] = trust_env
            captured["timeout"] = timeout

        # EN: Method __enter__ performs a focused step of the class workflow.
        # RU: Метод __enter__ выполняет целевой шаг в рабочем процессе класса.
        def __enter__(self) -> "FakeClient":
            return self

        # EN: Method __exit__ performs a focused step of the class workflow.
        # RU: Метод __exit__ выполняет целевой шаг в рабочем процессе класса.
        def __exit__(self, exc_type, exc_value, traceback) -> None:
            return None

        # EN: Method post performs a focused step of the class workflow.
        # RU: Метод post выполняет целевой шаг в рабочем процессе класса.
        def post(self, url: str, *, json: dict[str, object]) -> FakeResponse:
            captured["url"] = url
            captured["json"] = json
            return FakeResponse()

    monkeypatch.setattr("app.services.llm_service.httpx.Client", FakeClient)

    service = LLMService(
        Settings(
            llm_provider="ollama",
            ollama_base_url="http://127.0.0.1:11434",
            ollama_model="qwen2.5:7b",
            llm_temperature=0.15,
            llm_timeout=12.5,
        )
    )

    answer = service.compose_answer("What is the remote work policy?", "Employees may work remotely two days per week.")

    assert answer == "Use only the provided context."
    assert captured["url"] == "http://127.0.0.1:11434/api/chat"
    payload = captured["json"]
    assert isinstance(payload, dict)
    assert payload["model"] == "qwen2.5:7b"
    assert payload["stream"] is False
    assert payload["keep_alive"] == "1h"
    assert payload["options"] == {"temperature": 0.15}
    assert payload["messages"][0]["role"] == "system"
    assert payload["messages"][1]["role"] == "user"
    assert captured["trust_env"] is False
    assert captured["timeout"] == 12.5
