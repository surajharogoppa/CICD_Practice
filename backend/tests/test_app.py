import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "healthy"

def test_info(client):
    res = client.get("/api/info")
    assert res.status_code == 200
    assert "total_visits" in res.get_json()

def test_joke(client):
    res = client.get("/api/joke")
    assert res.status_code == 200
    data = res.get_json()
    assert "setup" in data
    assert "punchline" in data

def test_quote(client):
    res = client.get("/api/quote")
    assert res.status_code == 200
    assert "quote" in res.get_json()

def test_coinflip(client):
    res = client.get("/api/coinflip")
    assert res.status_code == 200
    assert res.get_json()["result"] in ["Heads", "Tails"]

def test_dice(client):
    res = client.get("/api/dice?sides=6&count=2")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data["rolls"]) == 2
    assert data["total"] == sum(data["rolls"])

def test_register(client):
    res = client.post("/api/users/register", json={
        "username": "testuser",
        "password": "testpass"
    })
    assert res.status_code == 201
    assert res.get_json()["username"] == "testuser"

def test_register_duplicate(client):
    client.post("/api/users/register", json={"username": "dupeuser", "password": "pass"})
    res = client.post("/api/users/register", json={"username": "dupeuser", "password": "pass"})
    assert res.status_code == 409

def test_login(client):
    client.post("/api/users/register", json={"username": "loginuser", "password": "mypass"})
    res = client.post("/api/users/login", json={"username": "loginuser", "password": "mypass"})
    assert res.status_code == 200

def test_login_wrong_password(client):
    client.post("/api/users/register", json={"username": "wrongpass", "password": "correct"})
    res = client.post("/api/users/login", json={"username": "wrongpass", "password": "wrong"})
    assert res.status_code == 401

def test_post_message(client):
    client.post("/api/users/register", json={"username": "msguser", "password": "pass"})
    res = client.post("/api/messages", json={"username": "msguser", "text": "Hello!"})
    assert res.status_code == 201

def test_word_count(client):
    res = client.post("/api/utils/wordcount", json={"text": "hello world flask"})
    assert res.status_code == 200
    assert res.get_json()["word_count"] == 3

def test_reverse(client):
    res = client.post("/api/utils/reverse", json={"text": "flask"})
    assert res.status_code == 200
    assert res.get_json()["reversed"] == "ksalf"