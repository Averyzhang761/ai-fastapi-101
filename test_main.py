import os
from types import SimpleNamespace
from unittest.mock import AsyncMock

os.environ.setdefault("OPENROUTER_API_KEY", "test-key")

from fastapi.testclient import TestClient

import main
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_rejects_missing_message():
    response = client.post("/chat", json={})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "message"]


def test_chat_returns_model_reply(monkeypatch):
    fake_response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(content="mock reply")
            )
        ]
    )
    fake_create = AsyncMock(return_value=fake_response)
    monkeypatch.setattr(
        main.client.chat.completions,
        "create",
        fake_create,
    )
    response = client.post(
        "/chat",
        json={"message": "hello"},
    )
    assert response.status_code == 200
    assert response.json() == {"reply": "mock reply"}
    fake_create.assert_awaited_once()
