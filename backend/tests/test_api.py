def test_health_endpoint(client) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_document_workflow_and_chat(client) -> None:
    upload_response = client.post(
        "/api/documents/upload",
        files={"file": ("handbook.txt", b"remote work policy allows two days per week in this example.", "text/plain")},
    )

    assert upload_response.status_code == 201
    upload_payload = upload_response.json()
    assert upload_payload["status"] == "processed"
    assert upload_payload["chunks_created"] >= 1

    document_id = upload_payload["document_id"]

    list_response = client.get("/api/documents")
    assert list_response.status_code == 200
    assert list_response.json()["documents"][0]["document_id"] == document_id

    detail_response = client.get(f"/api/documents/{document_id}")
    assert detail_response.status_code == 200
    assert detail_response.json()["document_id"] == document_id

    chat_response = client.post(
        "/api/chat/ask",
        json={"question": "What is the remote work policy?", "document_id": document_id},
    )

    assert chat_response.status_code == 200
    chat_payload = chat_response.json()
    assert chat_payload["question"] == "What is the remote work policy?"
    assert chat_payload["answer"]
    assert chat_payload["sources"]
