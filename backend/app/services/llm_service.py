from __future__ import annotations


class LLMService:
    def compose_answer(self, question: str, context: str) -> str:
        if not context.strip():
            return "No relevant document context was found yet."

        return (
            "This is a backend skeleton response. "
            f"Question: {question}. "
            f"Relevant context: {context[:400]}"
        )
