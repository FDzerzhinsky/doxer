"""
EN: File: tests/test_chunking_demo.py
EN: Purpose: Contains automated tests validating application behavior and edge cases.
EN: Scope: Documents key classes, functions, and execution flow in two languages.
EN: Notes: Keep comments concise and aligned with implementation changes.
RU: Файл: tests/test_chunking_demo.py
RU: Назначение: Содержит автотесты, проверяющие поведение приложения и граничные случаи.
RU: Область: Документирует ключевые классы, функции и поток выполнения на двух языках.
RU: Примечание: Держите комментарии лаконичными и синхронизированными с кодом.
"""

from app.utils.chunking import chunk_text


# EN: Function test_chunk_text_demo_outputs_chunks executes a specific reusable operation.
# RU: Функция test_chunk_text_demo_outputs_chunks выполняет конкретную переиспользуемую операцию.
def test_chunk_text_demo_outputs_chunks() -> None:
    sample_text = (
        "The AI Document Assistant ingests long documents, splits them into overlapping chunks, "
        "and prepares those chunks for retrieval. This demo test shows the actual chunk boundaries "
        "so you can visually confirm the slicing behavior before wiring FAISS."
    )

    chunks = chunk_text(sample_text, chunk_size=80, overlap=20)

    print("Chunk demo:")
    for index, chunk in enumerate(chunks, start=1):
        print(f"{index}: {chunk}")

    assert len(chunks) >= 3
    assert chunks[0].startswith("The AI Document Assistant")
    assert chunks[-1].endswith("wiring FAISS.")
