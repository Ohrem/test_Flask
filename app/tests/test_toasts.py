import pytest
from app import create_app
from model import db, User, ToastMessage

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()
        user1 = User(username="testuser")
        db.session.add(user1)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()


def test_create_toast(client):
    response = client.post("/toasts/", json={"text": "Test Toast", "user_id": None})
    assert response.status_code == 200
    data = response.get_json()
    assert "id" in data
    assert data["text"] == "Test Toast"
    assert data["user_id"] is None


def test_get_system_toasts(client):
    client.post("/toasts/", json={"text": "System Toast"})
    response = client.get("/toasts/")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1


def test_mark_toast_read(client):
    response = client.post("/toasts/", json={"text": "Test Toast"})
    toast_id = response.get_json()["id"]

    response = client.post("/toasts/mark-read", json={"id": [toast_id]})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Toasts marked as read"