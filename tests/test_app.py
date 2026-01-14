import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Baseball Team" in data

def test_signup_and_unregister():
    # Use a unique email to avoid conflicts
    test_email = "pytestuser@mergington.edu"
    activity = "Baseball Team"

    # Ensure not already signed up
    client.delete(f"/activities/{activity}/unregister?email={test_email}")

    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response.status_code == 200
    assert f"Signed up {test_email}" in response.json()["message"]

    # Try duplicate signup
    response_dup = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response_dup.status_code == 400

    # Unregister
    response_del = client.delete(f"/activities/{activity}/unregister?email={test_email}")
    assert response_del.status_code == 200
    assert f"Removed {test_email}" in response_del.json()["message"]

    # Unregister again (should fail)
    response_del2 = client.delete(f"/activities/{activity}/unregister?email={test_email}")
    assert response_del2.status_code == 404
