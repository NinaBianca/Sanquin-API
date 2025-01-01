import os
import sys

# Adjust the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import json
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app 
from models.user import User
from models.enums import FriendshipStatus

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


client = TestClient(app)

# Sample user data
sample_user = {
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

sample_updated_user = {
    "first_name": "Test",
    "last_name": "User",
    "username": "test_user",
    "password": "secure_password",
    "email": "test@example.com",
    "birthdate": "2000-01-01",
    "city": "Updated City",
    "current_points": 300,      
    "total_points": 300,
    "role": "user",
    "created_at": "2021-01-01T00:00:00Z",
}

# Sample friend data
sample_friend = {
    "id": 2,
    "first_name": "Test",
    "last_name": "Friend",
    "username": "test_friend",
    "password": "secure_password",
    "email": "friend@example.com",    
    "birthdate": "2000-01-01",
    "city": "Friend City",
    "current_points": 200,
    "total_points": 200,
    "role": "user",
    "created_at": "2021-01-01T00:00:00Z",
}

# Sample friend request data
sample_friend_request = {
    "sender_id": 1,
    "receiver_id": 2,
    "status": FriendshipStatus.PENDING.value,
    "created_at": "2021-01-01T00:00:00Z",
}

# --- User Routes Tests ---

# Test for creating a user
@patch("routers.users.create_user", return_value=MagicMock(**sample_user))
@patch("services.user.check_user_exists_by_username", return_value=False)
@patch("services.user.check_user_exists_by_email", return_value=False)
def test_create_user_route(create_user, user_check, email_check):
    response = client.post("/users/", json=sample_user)
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"


# Test for creating a user with duplicate username
@patch("services.user.check_user_exists_by_username", return_value=True)
def test_create_user_route_duplicate(user_check):
    response = client.post("/users/", json=sample_user)
    assert response.status_code == 400
    assert response.json()["detail"] == f"Username '{sample_user['username']}' is already in use."

# Test for creating a user with duplicate email
@patch("services.user.check_user_exists_by_username", return_value=False)
@patch("services.user.check_user_exists_by_email", return_value=True)
def test_create_user_route_duplicate_email(user_check, email_check):
    response = client.post("/users/", json=sample_user)
    assert response.status_code == 400
    assert response.json()["detail"] == f"Email '{sample_user['email']}' is already in use."

# Test for creating a user server error handling
@patch("routers.users.create_user", side_effect=Exception("Server error"))
def test_create_user_route_server_error(user_check):
    response = client.post("/users/", json=sample_user)
    assert response.status_code == 500
    assert response.json()["detail"] == "An error occurred while creating the user."

# Test for getting a user by ID
@patch("routers.users.get_user_by_id", return_value=MagicMock(**sample_user))
@patch("services.user.check_user_exists", return_value=True)
def test_get_user_by_id_route(get_user_by_id, check_user_exists):
    response = client.get("/users/id/1")
    assert response.status_code == 200
    assert response.json()["message"] == "User retrieved successfully"
    assert 1 in response.json()["data"][0]

# Test for getting a user by ID when user does not exist
@patch("services.user.check_user_exists", return_value=False)
def test_get_user_by_id_route_not_found(check_user_exists):
    response = client.get("/users/id/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found with ID 999"
    
# Test for getting user by ID server error handling
@patch("routers.users.get_user_by_id", side_effect=Exception("Server error"))
def test_get_user_by_id_route_server_error(check_user_exists):
    response = client.get("/users/id/1")
    assert response.status_code == 500
    assert response.json()["detail"] == "An error occurred while retrieving the user."
    
# Test for getting a user by email and password
@patch("routers.users.get_user_by_email_and_password", return_value=MagicMock(**sample_user))
def test_get_user_by_email_and_password_route(get_user_by_email_and_password):
    email = sample_user["email"]
    response = client.get(f"/users/email/{email}", params={"password": sample_user["password"]})
    assert response.status_code == 200
    assert response.json()["message"] == "User retrieved successfully"
    assert email in response.json()["data"][4]

# Test for getting a user by email and password when user does not exist
@patch("services.user.get_user_by_email_and_password", return_value=None)
def test_get_user_by_email_and_password_route_not_found(get_user_by_email_and_password):
    email = "unknown@example.com"
    response = client.get(f"/users/email/{email}", params={"password": "wrong_password"})
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found with email and password combination"
    
# Test for getting a user by email and password server error handling
@patch("routers.users.get_user_by_email_and_password", side_effect=Exception("Server error"))
def test_get_user_by_email_and_password_route_server_error(get_user_by_email_and_password):
    email = sample_user["email"]
    response = client.get(f"/users/email/{email}", params={"password": sample_user["password"]})
    assert response.status_code == 500
    assert response.json()["detail"] == "An error occurred while retrieving the user."

# Test for getting a user by username
@patch("services.user.get_users_by_partial_username", return_value=[sample_user])
def test_get_user_by_username_route(get_users_by_partial_username):
    response = client.get(f"/users/username/{sample_user['username']}")
    assert response.status_code == 200
    assert response.json()["message"] == "Users retrieved successfully"
    assert response.json()["data"][0]["username"] == sample_user["username"]

# Test for getting a user by username when user does not exist
@patch("services.user.get_users_by_partial_username", return_value=[])
def test_get_user_by_username_route_not_found(get_users_by_partial_username):
    response = client.get(f"/users/username/unknown_user")
    assert response.status_code == 404
    assert response.json()["detail"] == "Users not found with partial username unknown_user"
    
# Test for getting a user by username server error handling
@patch("routers.users.get_users_by_partial_username", side_effect=Exception("Server error"))
def test_get_user_by_username_route_server_error(get_users_by_partial_username):
    response = client.get(f"/users/username/{sample_user['username']}")
    assert response.status_code == 500
    assert response.json()["detail"] == "An error occurred while retrieving users."

# Test for updating a user
@patch("routers.users.update_user", return_value=MagicMock(**sample_updated_user))
@patch("services.user.check_user_exists", return_value=True)
def test_update_user_route(check_user_exists, update_user):
    response = client.put("/users/update/1", json=sample_updated_user)
    assert response.status_code == 200
    assert response.json()["message"] == "User updated successfully"
    assert "Updated City" in response.json()["data"][6]

# Test for updating a user when user does not exist
@patch("services.user.check_user_exists", return_value=False)
def test_update_user_route_not_found(check_user_exists): 
    response = client.put("/users/update/999", json=sample_updated_user)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found with ID 999"
    
# Test for updating a user server error handling
@patch("services.user.check_user_exists", side_effect=Exception("Server error"))
def test_update_user_route_server_error(check_user_exists):
    response = client.put("/users/update/1", json=sample_updated_user)
    assert response.status_code == 500
    assert response.json()["detail"] == "An error occurred while updating the user."

# Test for deleting a user
@patch("routers.users.delete_user")
@patch("services.user.check_user_exists", return_value=True)
def test_delete_user_route(check_user_exists, delete_user):
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json()["message"] == "User with ID 1 has been deleted"

# Test for deleting a user when user does not exist
@patch("services.user.check_user_exists", return_value=False)
def test_delete_user_route_not_found(check_user_exists):
    response = client.delete("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found with ID 999"
    
# Test for deleting a user server error handling
@patch("routers.users.delete_user", side_effect=Exception("Server error"))
def test_delete_user_route_server_error(check_user_exists):
    response = client.delete("/users/1")
    assert response.status_code == 500
    assert response.json()["detail"] == "An error occurred while deleting the user."

# --- Friend Routes Tests ---

# Test for sending a friend request
@patch("routers.users.send_friend_request", return_value=sample_friend_request)
@patch("services.user.check_user_exists", return_value=True)
def test_send_friend_request_route(check_user_exists, send_friend_request):
    response = client.post("/users/1/friends/2")
    print(response.json())
    assert response.status_code == 200
    assert response.json()["message"] == "Friend request sent successfully"

# Test for sending a friend request when user or friend does not exist
@patch("services.user.check_user_exists", return_value=False)
def test_send_friend_request_route_user_not_found(check_user_exists):
    response = client.post("/users/1/friends/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found with ID 999"
    
# Test for sending a friend request server error handling
@patch("services.user.check_user_exists", side_effect=Exception("Server error"))
def test_send_friend_request_route_server_error(check_user_exists):
    response = client.post("/users/1/friends/2")
    assert response.status_code == 500
    assert response.json()["detail"] == "An error occurred while sending the friend request."

# Test for editing a friend request
@patch("routers.users.edit_friend_request", return_value=sample_friend_request)
@patch("services.user.check_user_exists", return_value=True)
def test_edit_friend_request_route(check_user_exists, edit_friend_request):
    response = client.put(f"/users/1/friends/2?status={FriendshipStatus.ACCEPTED.value}")
    print(response.json())
    assert response.status_code == 200
    assert response.json()["message"] == "Friend request updated successfully"

# Test for editing a friend request when user or friend does not exist
@patch("services.user.check_user_exists", return_value=False)
def test_edit_friend_request_route_user_not_found(check_user_exists):
    response = client.put(f"/users/1/friends/999?status={FriendshipStatus.ACCEPTED.value}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Friend request not found with IDs 1 and 999"
    
# Test for editing a friend request server error handling
@patch("routers.users.edit_friend_request", side_effect=Exception("Server error"))
def test_edit_friend_request_route_server_error(check_user_exists):
    response = client.put(f"/users/1/friends/2?status={FriendshipStatus.ACCEPTED.value}")
    assert response.status_code == 500
    assert response.json()["detail"] == "An error occurred while updating the friend request."

# Test for getting friends
@patch("routers.users.get_friends", return_value=[sample_friend])
@patch("services.user.check_user_exists", return_value=True)
def test_get_friends_route(check_user_exists, get_friends):
    response = client.get("/users/1/friends")
    assert response.status_code == 200
    assert response.json()["message"] == "Friends retrieved successfully"
    assert response.json()["data"][0]["username"] == sample_friend["username"]

# Test for getting friends when user does not exist
@patch("services.user.check_user_exists", return_value=False)
def test_get_friends_route_user_not_found(check_user_exists):
    response = client.get("/users/999/friends")
    assert response.status_code == 404
    assert response.json()["detail"] == "Friends not found for user with ID 999"
    
# Test for getting friends server error handling
@patch("routers.users.get_friends", side_effect=Exception("Server error"))
def test_get_friends_route_server_error(check_user_exists):
    response = client.get("/users/1/friends")
    assert response.status_code == 500
    assert response.json()["detail"] == "An error occurred while retrieving friends."

# Test for getting friend requests
@patch("routers.users.get_friend_requests", return_value=[sample_friend_request])
@patch("services.user.check_user_exists", return_value=True)
def test_get_friend_requests_route(check_user_exists, get_friend_requests):
    response = client.get("/users/1/friend-requests")
    print(response.json())
    assert response.status_code == 200
    assert response.json()["message"] == "Friend requests retrieved successfully"

# Test for getting friend requests when user does not exist
@patch("services.user.check_user_exists", return_value=False)
def test_get_friend_requests_route_user_not_found(check_user_exists):
    response = client.get("/users/999/friend-requests")
    assert response.status_code == 404
    assert response.json()["detail"] == "Friend requests not found for user with ID 999"
    
# Test for getting friend requests server error handling
@patch("routers.users.get_friend_requests", side_effect=Exception("Server error"))
def test_get_friend_requests_route_server_error(check_user_exists):
    response = client.get("/users/1/friend-requests")
    assert response.status_code == 500
    assert response.json()["detail"] == "An error occurred while retrieving friend requests."

# Test for getting sent requests
@patch("routers.users.get_sent_requests", return_value=[sample_friend_request])
@patch("services.user.check_user_exists", return_value=True)
def test_get_sent_requests_route(check_user_exists, get_sent_requests):
    response = client.get("/users/1/sent-requests")
    print(response.json())
    assert response.status_code == 200
    assert response.json()["message"] == "Sent requests retrieved successfully"
    
# Test for getting sent requests when user does not exist
@patch("services.user.check_user_exists", return_value=False)
def test_get_sent_requests_route_user_not_found(check_user_exists):
    response = client.get("/users/999/sent-requests")
    assert response.status_code == 404
    assert response.json()["detail"] == "Sent requests not found for user with ID 999"

# Test for getting sent requests server error handling
@patch("routers.users.get_sent_requests", side_effect=Exception("Server error"))
def test_get_sent_requests_route_server_error(check_user_exists):
    response = client.get("/users/1/sent-requests")
    assert response.status_code == 500
    assert response.json()["detail"] == "An error occurred while retrieving sent requests."

# Test for deleting a friend
@patch("routers.users.delete_friend")
@patch("services.user.check_user_exists", return_value=True)
def test_delete_friend_route(check_user_exists, delete_friend):
    response = client.delete("/users/1/friends/2")
    assert response.status_code == 200
    assert response.json()["message"] == "Friend with ID 2 has been removed"

# Test for deleting a friend when user does not exist
@patch("services.user.check_user_exists", return_value=False)
def test_delete_friend_route_user_not_found(check_user_exists):
    response = client.delete("/users/1/friends/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Friend not found with IDs 1 and 999"
    
# Test for deleting a friend server error handling
@patch("routers.users.delete_friend", side_effect=Exception("Server error"))
def test_delete_friend_route_server_error(check_user_exists):
    response = client.delete("/users/1/friends/2")
    assert response.status_code == 500
    assert response.json()["detail"] == "An error occurred while deleting the friend."
    