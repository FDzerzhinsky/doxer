from app.utils.chunking import chunk_text


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
