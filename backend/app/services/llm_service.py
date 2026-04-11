from __future__ import annotations

import httpx

from app.core.config import Settings, get_settings


class LLMServiceError(RuntimeError):
    pass


class LLMService:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    def compose_answer(self, question: str, context: str) -> str:
        if not context.strip():
            return "No relevant document context was found yet."

        provider = self.settings.llm_provider.strip().lower()
        if provider == "mock":
            return self._compose_mock_answer(question, context)
        if provider == "ollama":
            return self._compose_ollama_answer(question, context)

        raise LLMServiceError(f"Unsupported LLM provider: {self.settings.llm_provider}")

    def _compose_mock_answer(self, question: str, context: str) -> str:
        return (
            "This is a mock RAG response. "
            f"Question: {question}. "
            f"Relevant context: {context[:400]}"
        )

    def _compose_ollama_answer(self, question: str, context: str) -> str:
        payload = {
            "model": self.settings.ollama_model,
            "stream": False,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a careful retrieval-augmented assistant. "
                        "Use only the supplied context. "
                        "If the answer is not in the context, say so explicitly."
                    ),
                },
                {
                    "role": "user",
                    "content": self._build_prompt(question, context),
                },
            ],
            "options": {"temperature": self.settings.llm_temperature},
        }

        url = f"{self.settings.ollama_base_url.rstrip('/')}/api/chat"
        try:
            with httpx.Client(trust_env=False, timeout=self.settings.llm_timeout) as client:
                response = client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise LLMServiceError(f"Failed to query Ollama at {url}: {exc}") from exc

        message = data.get("message") or {}
        answer = str(message.get("content") or "").strip()
        if not answer:
            raise LLMServiceError("Ollama response did not include assistant content.")

        return answer

    @staticmethod
    def _build_prompt(question: str, context: str) -> str:
        return (
            "Answer the question using only the context below.\n\n"
            f"Question:\n{question}\n\n"
            f"Context:\n{context}\n\n"
            "Return a concise answer and mention when the context is insufficient."
        )
