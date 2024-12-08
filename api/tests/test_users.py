import os
import sys

# Adjust the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app 
from models.user import User

client = TestClient(app)

# Sample user data
sample_user = {
    "id": 1,
    "username": "test_user",
    "password": "secure_password",
    "email": "test@example.com",
    "birthdate": "2000-01-01",
    "city": "Test City",
    "points": 100,
    "role": "user",
}

# Sample friend data
sample_friend = {
    "id": 2,
    "username": "friend_user",
    "password": "friend_password",
    "email": "friend@example.com",
    "birthdate": "1999-01-01",
    "city": "Friend City",
    "points": 50,
    "role": "user",
}

# --- User Routes Tests ---

# Test for creating a user
@patch("routers.users.create_user" , return_value=User(**sample_user))
@patch("routers.users.check_user_exists_by_username", return_value=False)
def test_create_user_route(create_user, user_check):
    response = client.post("/users/", json=sample_user)
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"


# Test for creating a user with duplicate username
@patch("routers.users.check_user_exists_by_username", return_value=True)
def test_create_user_route_duplicate(user_check):
    response = client.post("/users/", json=sample_user)
    assert response.status_code == 400
    assert response.json()["detail"] == f"Username '{sample_user['username']}' is already in use."


# Test for getting a user by ID
@patch("routers.users.get_user_by_id" , return_value=User(**sample_user))
@patch("routers.users.check_user_exists", return_value=True)
def test_get_user_by_id_route(get_user_by_id, arg):
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["message"] == "User retrieved successfully"
    assert response.json()["data"]["username"] == sample_user["username"]


# Test for getting a user by ID when user does not exist
def test_get_user_by_id_route_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found with ID 999"


# Test for getting a user by username
@patch("routers.users.get_user_by_username" , return_value=User(**sample_user))
@patch("routers.users.check_user_exists", return_value=True)
def test_get_user_by_username_route(get_user_by_username, arg):
    response = client.get(f"/users/username/{sample_user['username']}")
    assert response.status_code == 200
    assert response.json()["message"] == "User retrieved successfully"
    assert response.json()["data"]["username"] == sample_user["username"]


# Test for getting a user by username when user does not exist
@patch("routers.users.check_user_exists", return_value=False)
def test_get_user_by_username_route_not_found(arg):
    response = client.get("/users/username/nonexistent_user")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found with username nonexistent_user"


# Test for updating a user
@patch("routers.users.update_user" , return_value=User(**{'city': 'Updated City'}))
@patch("routers.users.check_user_exists", return_value=True)
def test_update_user_route(arg, update_user):
    update_data = {"city": "Updated City"}
    response = client.put("/users/1", json=update_data)
    assert response.status_code == 200
    assert response.json()["message"] == "User updated successfully"
    assert response.json()["data"]["city"] == "Updated City"


# Test for updating a user when user does not exist
def test_update_user_route_not_found(): 
    update_data = {"city": "Updated City"}
    response = client.put("/users/999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found with ID 999"


# Test for deleting a user
@patch("routers.users.delete_user")
@patch("routers.users.check_user_exists", return_value=True)
def test_delete_user_route(arg, delete_user):
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json()["message"] == "User with ID 1 has been deleted"


# Test for deleting a user when user does not exist
def test_delete_user_route_not_found():
    response = client.delete("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found with ID 999"


# --- Friend Routes Tests ---

# Test for sending a friend request
@patch("routers.users.send_friend_request" , return_value={"sender_id": 1, "receiver_id": 2, "status": "PENDING"})
@patch("routers.users.check_user_exists", return_value=True)
def test_send_friend_request_route(arg, send_friend_request):
    response = client.post("/users/1/friends/2")
    assert response.status_code == 200
    assert response.json()["message"] == "Friend request sent successfully"


# Test for sending a friend request when user or friend does not exist
@patch("routers.users.check_user_exists", return_value=False)
def test_send_friend_request_route_user_not_found(arg):
    response = client.post("/users/1/friends/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found with ID 999"