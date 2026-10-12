from fastapi.testclient import TestClient
import src.database as database
from src.main import app


def make_client(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "lab7.sqlite3")
    return TestClient(app)


def test_rest_api_contract_and_crud(tmp_path, monkeypatch):
    with make_client(tmp_path, monkeypatch) as client:
        assert client.get("/health").status_code == 200
        assert client.get("/users").status_code == 200
        assert client.get("/statuses").status_code == 200
        assert client.get("/categories").status_code == 200

        listed = client.get("/requests")
        assert listed.status_code == 200
        assert len(listed.json()) >= 10

        created = client.post("/requests", json={
            "title": "ЛР7: проверка REST API",
            "description": "Создание тестовой заявки через API",
            "user_id": 1,
            "category_id": 1
        })
        assert created.status_code == 201
        request_id = created.json()["request_id"]

        detail = client.get(f"/requests/{request_id}")
        assert detail.status_code == 200
        assert detail.json()["request_id"] == request_id

        search = client.get("/requests", params={"search": "ЛР7: проверка REST API"})
        assert search.status_code == 200
        assert any(x["request_id"] == request_id for x in search.json())

        status_filter = client.get("/requests", params={"status_id": 1})
        assert status_filter.status_code == 200
        assert all(x["status_id"] == 1 for x in status_filter.json())

        category_filter = client.get("/requests", params={"category_id": 1})
        assert category_filter.status_code == 200
        assert all(x["category_id"] == 1 for x in category_filter.json())

        updated = client.patch(f"/requests/{request_id}", json={"title": "ЛР7: заявка изменена"})
        assert updated.status_code == 200
        assert updated.json()["title"] == "ЛР7: заявка изменена"

        changed = client.patch(f"/requests/{request_id}/status", json={"status_id": 2})
        assert changed.status_code == 200
        assert changed.json()["status_id"] == 2

        invalid = client.post("/requests", json={
            "title": "x", "description": "", "user_id": 1, "category_id": 1
        })
        assert invalid.status_code == 422
        assert client.get("/requests/999999").status_code == 404

        deleted = client.delete(f"/requests/{request_id}")
        assert deleted.status_code == 204
        assert client.get(f"/requests/{request_id}").status_code == 404


def test_invalid_related_id_returns_400(tmp_path, monkeypatch):
    with make_client(tmp_path, monkeypatch) as client:
        response = client.post("/requests", json={
            "title": "Проверка связи",
            "description": "Проверка несуществующего пользователя",
            "user_id": 999999,
            "category_id": 1
        })
        assert response.status_code == 400


def test_openapi_schema_is_available(tmp_path, monkeypatch):
    with make_client(tmp_path, monkeypatch) as client:
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "/requests" in schema["paths"]
        assert "get" in schema["paths"]["/requests"]
        assert "post" in schema["paths"]["/requests"]
        assert "delete" in schema["paths"]["/requests/{request_id}"]
