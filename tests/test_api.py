from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_chat_endpoint_valid():
    response = client.post("/api/chat", json={"message": "Hello World"})
    assert response.status_code == 200
    data = response.json()
    assert "Echo from Root Agent" in data["response"]
    assert "Hello World" in data["sanitized_input"]

def test_chat_endpoint_sanitization():
    # Test with HTML injection
    malicious_input = "<script>alert('xss')</script>"
    response = client.post("/api/chat", json={"message": malicious_input})
    assert response.status_code == 200
    data = response.json()
    # Check that tags are escaped
    assert "&lt;script&gt;" in data["sanitized_input"]
    assert "<script>" not in data["sanitized_input"]

def test_chat_endpoint_empty():
    # Test with empty message if allowed, or check handling
    response = client.post("/api/chat", json={"message": ""})
    assert response.status_code == 200
    data = response.json()
    assert data["sanitized_input"] == ""
