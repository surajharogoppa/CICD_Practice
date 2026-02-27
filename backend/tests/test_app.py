import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Flask CI/CD API" in response.data  # check HTML content instead

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"

def test_joke(client):
    response = client.get("/joke")
    assert response.status_code == 200
    data = response.get_json()
    assert "setup" in data
    assert "punchline" in data

def test_quote(client):
    response = client.get("/quote")
    assert response.status_code == 200
    data = response.get_json()
    assert "quote" in data
    assert "author" in data

def test_coinflip(client):
    response = client.get("/coinflip")
    assert response.status_code == 200
    assert response.get_json()["result"] in ["Heads", "Tails"]

def test_dice(client):
    response = client.get("/dice?sides=6&count=2")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["rolls"]) == 2
    assert data["total"] == sum(data["rolls"])

def test_register(client):
    response = client.post("/users/register", json={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 201
    assert response.get_json()["username"] == "testuser"

def test_register_duplicate(client):
    client.post("/users/register", json={"username": "dupeuser", "password": "pass"})
    response = client.post("/users/register", json={"username": "dupeuser", "password": "pass"})
    assert response.status_code == 409

def test_login(client):
    client.post("/users/register", json={"username": "loginuser", "password": "mypass"})
    response = client.post("/users/login", json={"username": "loginuser", "password": "mypass"})
    assert response.status_code == 200

def test_login_wrong_password(client):
    client.post("/users/register", json={"username": "wrongpass", "password": "correct"})
    response = client.post("/users/login", json={"username": "wrongpass", "password": "wrong"})
    assert response.status_code == 401

def test_post_message(client):
    client.post("/users/register", json={"username": "msguser", "password": "pass"})
    response = client.post("/messages", json={"username": "msguser", "text": "Hello!"})
    assert response.status_code == 201

def test_word_count(client):
    response = client.post("/utils/wordcount", json={"text": "hello world flask"})
    assert response.status_code == 200
    assert response.get_json()["word_count"] == 3

def test_reverse(client):
    response = client.post("/utils/reverse", json={"text": "flask"})
    assert response.status_code == 200
    assert response.get_json()["reversed"] == "ksalf"