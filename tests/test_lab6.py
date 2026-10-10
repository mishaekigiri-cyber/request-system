from fastapi.testclient import TestClient
import src.database as database
from src.main import app


def client_for(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.sqlite3")
    return TestClient(app)


def test_seed_has_at_least_ten_requests(tmp_path, monkeypatch):
    with client_for(tmp_path, monkeypatch) as client:
        response = client.get("/requests")
        assert response.status_code == 200
        assert len(response.json()) >= 10
        assert len(client.get("/users").json()) >= 4
        assert len(client.get("/categories").json()) >= 4


def test_create_view_edit_and_change_status(tmp_path, monkeypatch):
    with client_for(tmp_path, monkeypatch) as client:
        created = client.post("/requests", json={"title":"Проверка сети", "description":"Нужно проверить подключение к сети", "user_id":1, "category_id":3})
        assert created.status_code == 201
        request_id = created.json()["request_id"]
        assert created.json()["status"] == "Новая"
        detail = client.get(f"/requests/{request_id}")
        assert detail.status_code == 200
        updated = client.patch(f"/requests/{request_id}", json={"title":"Проверка сети аудитории"})
        assert updated.status_code == 200
        assert updated.json()["title"] == "Проверка сети аудитории"
        changed = client.patch(f"/requests/{request_id}/status", json={"status_id":2})
        assert changed.status_code == 200
        assert changed.json()["status"] == "В работе"


def test_search_and_filters(tmp_path, monkeypatch):
    with client_for(tmp_path, monkeypatch) as client:
        response = client.get("/requests", params={"search":"принтер"})
        assert response.status_code == 200
        assert any("принтер" in x["title"].lower() for x in response.json())
        filtered = client.get("/requests", params={"status_id":1})
        assert filtered.status_code == 200
        assert all(x["status_id"] == 1 for x in filtered.json())


def test_not_found_and_invalid_data(tmp_path, monkeypatch):
    with client_for(tmp_path, monkeypatch) as client:
        assert client.get("/requests/999999").status_code == 404
        invalid = client.post("/requests", json={"title":"x", "description":"", "user_id":1, "category_id":1})
        assert invalid.status_code == 422
        missing_user = client.post("/requests", json={"title":"Важная заявка", "description":"Проверка несуществующего заявителя", "user_id":999, "category_id":1})
        assert missing_user.status_code == 400
        assert client.get("/health").json() == {"status":"ok"}
