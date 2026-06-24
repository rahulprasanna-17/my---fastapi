from fastapi.testclient import TestClient
from rahul import app

client = TestClient(app)

def test_hello():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello! I am your FastAPI waiter! 🍕"}

def test_greet():
    response = client.get("/greet/Rahul")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Rahul! Welcome to my API! 🎉"}

def test_orders_without_api_key():
    response = client.get("/orders")
    assert response.status_code == 401

def test_orders_with_api_key():
    response = client.get("/orders", headers={"api-key": "rahul1234"})
    assert response.status_code == 200