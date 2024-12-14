import os
import sys

# Adjust the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app 

client = TestClient(app)

# Sample post data
sample_post = {
    "id": 1,
    "content": "This is a test post",
    "user_id": 1,
    "created_at": "2021-01-01T00:00:00+00:00",
}

# Sample kudos data
sample_kudos = {
    "id": 1,
    "post_id": 1,
    "user_id": 1,

}


# Test for creating a post
@patch("routers.posts.create_post", return_value=sample_post)
@patch("routers.posts.check_user_exists", return_value=True)
def test_create_post_route(create_post, check_user_exists):
    response = client.post("/posts/", json=sample_post)
    assert response.status_code == 200
    assert response.json()["data"]["content"] == "This is a test post"
    assert response.json()["data"]["user_id"] == 1

# Test for getting posts by user ID
@patch("routers.posts.get_posts_by_user_id", return_value=[sample_post])
@patch("routers.posts.check_user_exists", return_value=True)
def test_get_posts_by_user_id_route(get_posts_by_user_id, check_user_exists):
    response = client.get("/posts/user/1")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["content"] == "This is a test post"
    assert response.json()["data"][0]["user_id"] == 1

# Test for deleting a post
@patch("routers.posts.delete_post", return_value=True)
@patch("routers.posts.check_post_exists", return_value=True)
def test_delete_post_route(delete_post, check_post_exists):
    response = client.delete("/posts/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Post deleted successfully"

# Test for adding kudos to a post
@patch("routers.posts.add_kudos", return_value=sample_kudos)
@patch("routers.posts.check_post_exists", return_value=True)
@patch("routers.posts.check_user_exists", return_value=True)
def test_add_kudos_route(add_kudos, check_post_exists, check_user_exists):
    response = client.post("/posts/1/kudos", json=sample_kudos)
    assert response.status_code == 200
    assert response.json()["message"] == "Kudos added successfully"

# Test for getting kudos by post ID
@patch("routers.posts.get_kudos_by_post_id", return_value=[sample_kudos])
@patch("routers.posts.check_post_exists", return_value=True)
def test_get_kudos_by_post_id_route(get_kudos_by_post_id, check_post_exists):
    response = client.get("/posts/1/kudos")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["post_id"] == 1
    assert response.json()["data"][0]["user_id"] == 1

# Test for deleting kudos
@patch("routers.posts.delete_kudos", return_value=True)
@patch("routers.posts.check_post_exists", return_value=True)
@patch("routers.posts.check_user_exists", return_value=True)
@patch("routers.posts.check_kudos_exists", return_value=True)
def test_delete_kudos_route(delete_kudos, check_post_exists, check_user_exists, check_kudos_exists):
    response = client.delete("/posts/1/kudos/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Kudos deleted successfully"

# Test for getting friends' posts
@patch("routers.posts.get_friends_posts", return_value=[sample_post])
@patch("routers.posts.check_user_exists", return_value=True)
def test_get_friends_posts_route(get_friends_posts, check_user_exists):
    response = client.get("/posts/friends/1")
    assert response.status_code == 200
    assert response.json()["data"][0]["content"] == "This is a test post"
    assert response.json()["data"][0]["user_id"] == 1