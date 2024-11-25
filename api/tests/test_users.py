import sys
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from fastapi import HTTPException, status as HTTP_500_INTERNAL_SERVER_ERROR

# Adjust the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app
from models.user.user import UserModel, DonationType
from models.user.update_user import UpdateUserModel
from models.user.user_collection import UserCollection

client = TestClient(app)
user_data = UserModel(id=1, username="test", email="test@email.com", password="test", donation_type=DonationType.BLOOD).model_dump()
existing_username_data = UserModel(id=2, username="test", email="new@email.com", password="test", donation_type=DonationType.BLOOD).model_dump()
existing_email_data = UserModel(id=3, username="new", email="test@email.com", password="test", donation_type=DonationType.BLOOD).model_dump()
update_user_data = UpdateUserModel(username="test", email="test1@email.com", password="test", donation_type=DonationType.PLASMA).model_dump()

@patch("routers.users.user_collection")
def test_read_users(mock_user_collection):
    mock_user_collection.find.return_value.skip.return_value.limit.return_value.to_list = AsyncMock(return_value=[])
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == {
        "status": 200,
        "data": [],
        "message": "Users retrieved successfully"
    }

@patch("routers.users.user_collection")
def test_create_user(mock_user_collection):
    mock_user_collection.insert_one = AsyncMock(return_value=user_data)
    mock_user_collection.find_one = AsyncMock(return_value=None)  # Convert SecretStr to string
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json() == {
        "status": 200,
        "data": user_data,
        "message": "User created successfully"
    }

@patch("routers.users.user_collection")
def test_create_user_existing_username(mock_user_collection):
    mock_user_collection.insert_one = AsyncMock(return_value=user_data)
    mock_user_collection.find_one = AsyncMock(return_value=existing_username_data)
    response = client.post("/users/", json=existing_username_data)
    assert response.status_code == 500
    assert response.json() == {
        "detail": "An error occurred: 500: Username already exists"
    }

@patch("routers.users.user_collection")
def test_create_user_existing_email(mock_user_collection):
    mock_user_collection.find_one = AsyncMock(return_value=user_data)
    response = client.post("/users/", json=existing_email_data)
    assert response.status_code == 500
    assert response.json() == {
        "detail": "An error occurred: 500: Email already exists"
    }


@patch("routers.users.user_collection")
def test_login_user(mock_user_collection):
    mock_user_collection.find_one = AsyncMock(return_value=UserModel(username="test", email="test@email.com", password="test", donation_type=DonationType.BLOOD).model_dump())
    response = client.post("/users/login", json=user_data)
    assert response.status_code == 200
    assert response.json() == {
        "status": 200,
        "data": user_data,
        "message": "User logged in successfully"
    }

@patch("routers.users.user_collection")
def test_login_user_invalid(mock_user_collection):
    mock_user_collection.find_one = AsyncMock(return_value=None)
    response = client.post("/users/login", json=user_data)
    assert response.status_code == 500
    assert response.json() == {
        "detail": "An error occurred: 500: Invalid username or password"
    }

@patch("routers.users.user_collection")
def test_update_user(mock_user_collection):
    mock_user_collection.find_one = AsyncMock(return_value=user_data)
    mock_user_collection.update_one = AsyncMock(return_value=user_data)
    response = client.put(f"/users/{1}", json=update_user_data)
    assert response.status_code == 200
    assert response.json() == {
        "status": 200,
        "data": user_data,
        "message": "User updated successfully"
    }

@patch("routers.users.user_collection")
def test_update_user_not_found(mock_user_collection):
    mock_user_collection.find_one = AsyncMock(return_value=None)
    response = client.put("/users/1", json=update_user_data)
    assert response.status_code == 500
    assert response.json() == {'detail': 'An error occurred: 500: User not found'}