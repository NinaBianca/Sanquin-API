import os
import sys

# Adjust the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import json
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app 
from models.user import User

client = TestClient(app)

# Sample user data
sample_user = {
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
}

# Sample friend data
sample_friend = {
    "first_name": "Test",
    "last_name": "Friend",
    "username": "test_friend",
    "password": "secure_password",
    "email": "friend@email.com",	
    "birthdate": "2000-01-01",
    "city": "Friend City",
    "current_points": 200,
    "total_points": 200,
    "role": "user",
}

# --- User Routes Tests ---

# Test for creating a user
@patch("routers.users.create_user" , return_value=User(**sample_user))
@patch("routers.users.check_user_exists_by_username", return_value=False)
@patch("routers.users.check_user_exists_by_email", return_value=False)
def test_create_user_route(create_user, user_check, email_chck):
    response = client.post("/users/", json=sample_user)
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"


# Test for creating a user with duplicate username
@patch("routers.users.check_user_exists_by_username", return_value=True)
def test_create_user_route_duplicate(user_check):
    response = client.post("/users/", json=sample_user)
    assert response.status_code == 400
    assert response.json()["detail"] == f"Username '{sample_user['username']}' is already in use."

# Test for creating a user with duplicate email
@patch("routers.users.check_user_exists_by_username", return_value=False)
@patch("routers.users.check_user_exists_by_email", return_value=True)
def test_create_user_route_duplicate_email(user_check, email_check):
    response = client.post("/users/", json=sample_user)
    assert response.status_code == 400
    assert response.json()["detail"] == f"Email '{sample_user['email']}' is already in use."

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
    
    
# Test for getting a user by email and password
@patch("routers.users.get_user_by_email_and_password" , return_value=User(**sample_user))
def test_get_user_by_email_and_password_route(get_user_by_email_and_password):
    email = sample_user["email"]
    response = client.get("/users/email/{email}", params={"password":sample_user["password"]})
    assert response.status_code == 200
    assert response.json()["message"] == "User retrieved successfully"
    assert response.json()["data"]["email"] == sample_user["email"]
    

# Test for getting a user by email and password when user does not exist
def test_get_user_by_email_and_password_route_not_found():
    email = "blup"
    response = client.get("/users/email/{email}", params={"password":"blup"})
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found with email and password combination"



# Test for getting a user by username
@patch("routers.users.get_users_by_partial_username" , return_value=[User(**sample_user)])
def test_get_user_by_username_route(get_user_by_username):
    response = client.get(f"/users/username/{sample_user['username']}")
    assert response.status_code == 200
    assert response.json()["message"] == "Users retrieved successfully"
    assert response.json()["data"][0] == User(**sample_user).model_dump()
    
# @patch("routers.users.get_users_by_partial_username" , return_value=[])
def test_get_user_by_username_route_not_found():
    response = client.get(f"/users/username/unknown_user")
    assert response.status_code == 404
    assert response.json()["detail"] == "Users not found with partial username unknown_user"


# Test for updating a user
@patch("routers.users.update_user" , return_value=User(**{'city': 'Updated City'}))
@patch("routers.users.check_user_exists", return_value=True)
def test_update_user_route(arg, update_user):
    update_data = {"city": "Updated City", "id": 1}
    response = client.put("/users/1", json=update_data)
    assert response.status_code == 200
    assert response.json()["message"] == "User updated successfully"
    assert response.json()["data"]["city"] == "Updated City"


# Test for updating a user when user does not exist
def test_update_user_route_not_found(): 
    update_data = {"city": "Updated City", "id": 999}
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