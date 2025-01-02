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
}

sample_challenge_response = {
    "id": 1,
    "title": "Test Challenge",
    "description": "This is a test challenge",
    "location": "Test Location",
    "start": "2021-01-01T00:00:00+00:00",
    "end": "2021-01-31T00:00:00+00:00",
    "goal": 100,
}

# Sample challenge user data
sample_challenge_user = {
    "challenge_id": 1,
    "user_id": 1,
    "status": "active",
}

sample_user_response = {
    "id": 1,
    "first_name": "Test",
    "last_name": "User",
    "username": "test_user",
    "password": "secure_password",
    "email": "test@example.com",
    "birthdate": "2000-01-01",
    "city": "Test City",
    "current_points": 200,      
    "total_points": 200,
    "role": "user",
    "created_at": "2021-01-01T00:00:00Z",
}

# --- Challenge Routes Tests ---
# Test for creating a challenge
@patch("routers.challenges.create_challenge", return_value=sample_challenge_response)
def test_create_challenge_route(create_challenge):
    response = client.post("/challenges/", json=sample_challenge)
    assert response.status_code == 200
    assert response.json()["message"] == "Challenge created successfully"
    
# Test for creating a challenge service error
@patch("routers.challenges.create_challenge", side_effect=Exception("An error occurred while creating the challenge"))
def test_create_challenge_route_error(create_challenge):
    response = client.post("/challenges/", json=sample_challenge)
    assert response.status_code == 500
    assert "An error occurred while creating the challenge" in response.json()["detail"]


# Test for getting all challenges
@patch("routers.challenges.get_challenges", return_value=[sample_challenge_response])
def test_read_challenges_route(get_challenges):
    response = client.get("/challenges/")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["title"] == "Test Challenge"
    
# Test for getting all challenges service error
@patch("routers.challenges.get_challenges", side_effect=Exception("An error occurred while retrieving the challenges"))
def test_read_challenges_route_error(get_challenges):
    response = client.get("/challenges/")
    assert response.status_code == 500
    assert "An error occurred while retrieving the challenges" in response.json()["detail"]

# Test for getting a challenge by ID
@patch("routers.challenges.get_challenge_by_id", return_value=sample_challenge_response)
def test_get_challenge_route(get_challenge_by_id):
    response = client.get("/challenges/1")
    assert response.status_code == 200
    assert "Test Challenge" in response.json()["data"][0]


@patch("services.challenge.check_challenge_exists", return_value=False)
def test_get_challenge_route_not_found(check_challenge_exists):
    response = client.get("/challenges/2")
    assert response.status_code == 500
    assert "An error occurred while retrieving the challenge" in response.json()["detail"]

# Test for updating a challenge
@patch("routers.challenges.update_challenge", return_value=sample_challenge_response)
def test_update_challenge_route(update_challenge):
    response = client.put("/challenges/1", json=sample_challenge)
    assert response.status_code == 200
    assert "Test Challenge" in response.json()["data"][0] 

@patch("services.challenge.check_challenge_exists", return_value=False)
def test_update_challenge_route_not_found(check_challenge_exists):
    response = client.put("/challenges/2", json=sample_challenge)
    assert response.status_code == 500
    assert "An error occurred while updating the challenge" in response.json()["detail"]


# Test for deleting a challenge
@patch("routers.challenges.delete_challenge", return_value=True)
def test_remove_challenge_route(delete_challenge):
    response = client.delete("/challenges/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Challenge deleted successfully"

@patch("services.challenge.check_challenge_exists", return_value=False)
def test_remove_challenge_route_not_found(check_challenge_exists):
    response = client.delete("/challenges/2")
    assert response.status_code == 500
    assert "An error occurred while deleting the challenge" in response.json()["detail"]

# Test for adding a user to a challenge
@patch("routers.challenges.add_user_to_challenge")
@patch("routers.challenges.check_user_exists", return_value=True)
def test_add_user_to_challenge_route(add_user_to_challenge, check_user_exists):
    response = client.post("/challenges/1/user/1")
    assert response.status_code == 200
    assert response.json()["message"] == "User added to challenge successfully"


@patch("routers.challenges.check_user_exists", return_value=False)
def test_add_user_to_challenge_route_user_not_found(check_user_exists):
    response = client.post("/challenges/1/user/2")
    assert response.status_code == 404
    assert "User not found with ID 2" in response.json()["detail"]

@patch("routers.challenges.check_user_exists", return_value=True)
@patch("services.challenge.check_challenge_exists", return_value=False)
def test_add_user_to_challenge_route_challenge_not_found(check_user_exists, check_challenge_exists):
    response = client.post("/challenges/2/user/1")
    assert response.status_code == 500
    assert "An error occurred while adding user to challenge" in response.json()["detail"]


# Test for getting challenges by user ID
@patch("routers.challenges.get_challenges_by_user_id", return_value=[sample_challenge_response])
@patch("routers.challenges.check_user_exists", return_value=True)
def test_read_challenges_by_user_id_route(get_challenges_by_user_id, check_user_exists):
    response = client.get("/challenges/user/1")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["title"] == "Test Challenge"

@patch("routers.challenges.check_user_exists", return_value=False)
def test_read_challenges_by_user_id_route_not_found(check_user_exists):
    response = client.get("/challenges/user/2")
    assert response.status_code == 404
    assert "User not found with ID 2" in response.json()["detail"]
    
# Test for getting challenges by user ID service error
@patch("routers.challenges.check_user_exists", return_value=True)
@patch("services.challenge.get_challenges_by_user_id", side_effect=Exception("An error occurred while retrieving the challenges"))
def test_read_challenges_by_user_id_route_error(check_user_exists, get_challenges_by_user_id):
    response = client.get("/challenges/user/1")
    assert response.status_code == 500
    assert "An error occurred while retrieving the challenges" in response.json()["detail"]

# Test for getting users by challenge ID
@patch("routers.challenges.get_users_by_challenge_id", return_value=[sample_user_response])
def test_get_users_by_challenge_id_route(get_users_by_challenge_id):
    response = client.get("/challenges/1/users")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1

@patch("services.challenge.check_challenge_exists", return_value=False)
def test_get_users_by_challenge_id_route_not_found(check_challenge_exists):
    response = client.get("/challenges/2/users")
    assert response.status_code == 500
    assert "An error occurred while retrieving the users" in response.json()["detail"]

# Test for deleting a user from a challenge
@patch("routers.challenges.delete_user_from_challenge", return_value=True)
@patch("routers.challenges.check_user_exists", return_value=True)
def test_delete_user_from_challenge_route(delete_user_from_challenge, check_user_exists):
    response = client.delete("/challenges/1/user/1")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted from challenge successfully"

@patch("routers.challenges.check_user_exists", return_value=False)
def test_delete_user_from_challenge_route_user_not_found(check_user_exists):
    response = client.delete("/challenges/1/user/2")
    assert response.status_code == 404
    assert "User not found with ID 2" in response.json()["detail"]


@patch("routers.challenges.check_user_exists", return_value=True)
@patch("services.challenge.check_challenge_exists", return_value=False)
def test_delete_user_from_challenge_route_challenge_not_found(check_user_exists, check_challenge_exists):
    response = client.delete("/challenges/2/user/1")
    assert response.status_code == 500
    assert "An error occurred while deleting user from challenge" in response.json()["detail"]