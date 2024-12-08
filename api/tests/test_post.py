import os
import sys

# Adjust the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app  # Assuming your FastAPI app is in main.py
from models.post import Post
from models.kudos import Kudos

client = TestClient(app)

# Test for creating a post
@patch("routers.posts.create_post", return_value=Post(**{'title': 'Test Post', 'content': 'This is a test post', 'user_id': 1}))
def test_create_post_route(create_post):
    post_data = {"title": "Test Post", "content": "This is a test post", "user_id": 1}
    response = client.post("/posts/", json=post_data)
    assert response.status_code == 201
    assert response.json()["title"] == "Test Post"
    assert response.json()["content"] == "This is a test post"
    assert response.json()["user_id"] == 1

# Test for getting posts by user ID
@patch("routers.posts.get_posts_by_user_id", return_value=[Post(**{'title': 'Test Post', 'content': 'This is a test post', 'user_id': 1})])
def test_get_posts_by_user_id_route(get_posts_by_user_id):
    response = client.get("/posts/user/1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Test Post"
    assert response.json()[0]["content"] == "This is a test post"
    assert response.json()[0]["user_id"] == 1

# Test for deleting a post
@patch("routers.posts.delete_post", return_value=Post(**{'title': 'Test Post', 'content': 'This is a test post', 'user_id': 1}))
def test_delete_post_route(delete_post):
    response = client.delete("/posts/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Post deleted successfully"
    assert response.json()["title"] == "Test Post"
    assert response.json()["content"] == "This is a test post"
    assert response.json()["user_id"] == 1

# Test for adding kudos to a post
@patch("routers.posts.add_kudos", return_value=Kudos(**{'post_id': 1, 'user_id': 1}))
def test_add_kudos_route(add_kudos):
    kudos_data = {"post_id": 1, "user_id": 1}
    response = client.post("/posts/1/kudos", json=kudos_data)
    assert response.status_code == 201
    assert response.json()["post_id"] == 1
    assert response.json()["user_id"] == 1

# Test for getting kudos by post ID
@patch("routers.posts.get_kudos_by_post_id", return_value=[Kudos(**{'post_id': 1, 'user_id': 1})])
def test_get_kudos_by_post_id_route(get_kudos_by_post_id):
    response = client.get("/posts/1/kudos")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["post_id"] == 1
    assert response.json()[0]["user_id"] == 1

# Test for deleting kudos
@patch("routers.posts.delete_kudos", return_value=Kudos(**{'post_id': 1, 'user_id': 1}))
def test_delete_kudos_route(delete_kudos):
    response = client.delete("/posts/1/kudos/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Kudos deleted successfully"
    assert response.json()["post_id"] == 1
    assert response.json()["user_id"] == 1