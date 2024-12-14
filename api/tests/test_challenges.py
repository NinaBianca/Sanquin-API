import os
import sys

# Adjust the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Sample challenge data
sample_challenge = {
    "title": "Test Challenge",
    "description": "This is a test challenge",
    "location": "Test Location",
    "start": "2021-01-01T00:00:00+00:00",
    "end": "2021-01-31T00:00:00+00:00",
    "goal": 100,
    "status": "active",
}

# Sample challenge user data
sample_challenge_user = {
    "challenge_id": 1,
    "user_id": 1,
    "status": "active",
}

# --- Challenge Routes Tests ---
# Test for creating a challenge
@patch("routers.challenges.create_challenge", return_value=sample_challenge)
def test_create_challenge_route(create_challenge):
    response = client.post("/challenges/", json=sample_challenge)
    assert response.status_code == 200
    assert response.json()["message"] == "Challenge created successfully"


# Test for getting all challenges
@patch("routers.challenges.get_challenges", return_value=[sample_challenge])
def test_read_challenges_route(get_challenges):
    response = client.get("/challenges/")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["title"] == "Test Challenge"

# Test for getting a challenge by ID
@patch("routers.challenges.get_challenge_by_id", return_value=sample_challenge)
@patch("routers.challenges.check_challenge_exists", return_value=True)
def test_get_challenge_route(get_challenge_by_id, check_challenge_exists):
    response = client.get("/challenges/1")
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "Test Challenge"

@patch("routers.challenges.get_challenge_by_id", return_value=sample_challenge)
@patch("routers.challenges.check_challenge_exists", return_value=False)
def test_get_challenge_route_not_found(get_challenge_by_id, check_challenge_exists):
    response = client.get("/challenges/2")
    assert response.status_code == 404
    assert response.json()["detail"] == "Challenge not found with ID 2"

# Test for updating a challenge
@patch("routers.challenges.update_challenge", return_value=sample_challenge)
@patch("routers.challenges.check_challenge_exists", return_value=True)
def test_update_challenge_route(update_challenge, check_challenge_exists):
    response = client.put("/challenges/1", json=sample_challenge)
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "Test Challenge"

@patch("routers.challenges.update_challenge", return_value=sample_challenge)
@patch("routers.challenges.check_challenge_exists", return_value=False)
def test_update_challenge_route_not_found(update_challenge, check_challenge_exists):
    response = client.put("/challenges/2", json=sample_challenge)
    assert response.status_code == 404
    assert response.json()["detail"] == "Challenge not found with ID 2"


# Test for deleting a challenge
@patch("routers.challenges.delete_challenge", return_value=True)
@patch("routers.challenges.check_challenge_exists", return_value=True)
def test_remove_challenge_route(delete_challenge, check_challenge_exists):
    response = client.delete("/challenges/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Challenge deleted successfully"

@patch("routers.challenges.delete_challenge", return_value=True)
@patch("routers.challenges.check_challenge_exists", return_value=False)
def test_remove_challenge_route_not_found(delete_challenge, check_challenge_exists):
    response = client.delete("/challenges/2")
    assert response.status_code == 404
    assert response.json()["detail"] == "Challenge not found with ID 2"

# Test for adding a user to a challenge
@patch("routers.challenges.add_user_to_challenge")
@patch("routers.challenges.check_user_exists", return_value=True)
@patch("routers.challenges.check_challenge_exists", return_value=True)
def test_add_user_to_challenge_route(add_user_to_challenge, check_user_exists, check_challenge_exists):
    response = client.post("/challenges/1/user/1")
    assert response.status_code == 200
    assert response.json()["message"] == "User added to challenge successfully"

@patch("routers.challenges.add_user_to_challenge")
@patch("routers.challenges.check_user_exists", return_value=False)
def test_add_user_to_challenge_route_user_not_found(add_user_to_challenge, check_user_exists):
    response = client.post("/challenges/1/user/2")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found with ID 2"

@patch("routers.challenges.add_user_to_challenge")
@patch("routers.challenges.check_user_exists", return_value=True)
@patch("routers.challenges.check_challenge_exists", return_value=False)
def test_add_user_to_challenge_route_challenge_not_found(add_user_to_challenge, check_user_exists, check_challenge_exists):
    response = client.post("/challenges/2/user/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Challenge not found with ID 2"


# Test for getting challenges by user ID
@patch("routers.challenges.get_challenges_by_user_id", return_value=[sample_challenge])
@patch("routers.challenges.check_user_exists", return_value=True)
def test_read_challenges_by_user_id_route(get_challenges_by_user_id, check_user_exists):
    response = client.get("/challenges/user/1")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["title"] == "Test Challenge"

@patch("routers.challenges.get_challenges_by_user_id", return_value=[sample_challenge])
@patch("routers.challenges.check_user_exists", return_value=False)
def test_read_challenges_by_user_id_route_not_found(get_challenges_by_user_id, check_user_exists):
    response = client.get("/challenges/user/2")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found with ID 2"

# Test for getting users by challenge ID
@patch("routers.challenges.get_users_by_challenge_id", return_value=[sample_challenge_user])
@patch("routers.challenges.check_challenge_exists", return_value=True)
def test_get_users_by_challenge_id_route(get_users_by_challenge_id, check_challenge_exists):
    response = client.get("/challenges/1/users")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["user_id"] == 1

@patch("routers.challenges.get_users_by_challenge_id", return_value=[sample_challenge_user])
@patch("routers.challenges.check_challenge_exists", return_value=False)
def test_get_users_by_challenge_id_route_not_found(get_users_by_challenge_id, check_challenge_exists):
    response = client.get("/challenges/2/users")
    assert response.status_code == 404
    assert response.json()["detail"] == "Challenge not found with ID 2"

# Test for deleting a user from a challenge
@patch("routers.challenges.delete_user_from_challenge")
@patch("routers.challenges.check_user_exists", return_value=True)
@patch("routers.challenges.check_challenge_exists", return_value=True)
def test_delete_user_from_challenge_route(delete_user_from_challenge, check_user_exists, check_challenge_exists):
    response = client.delete("/challenges/1/user/1")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted from challenge successfully"

@patch("routers.challenges.delete_user_from_challenge")
@patch("routers.challenges.check_user_exists", return_value=False)
def test_delete_user_from_challenge_route_user_not_found(delete_user_from_challenge, check_user_exists):
    response = client.delete("/challenges/1/user/2")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found with ID 2"

@patch("routers.challenges.delete_user_from_challenge")
@patch("routers.challenges.check_user_exists", return_value=True)
@patch("routers.challenges.check_challenge_exists", return_value=False)
def test_delete_user_from_challenge_route_challenge_not_found(delete_user_from_challenge, check_user_exists, check_challenge_exists):
    response = client.delete("/challenges/2/user/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Challenge not found with ID 2"