import os
import sys

# Adjust the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app 

client = TestClient(app)

# Sample kudos data
sample_kudos = {
    "post_id": 1,
    "user_id": 1
}

sample_kudos_response = {
    "id": 1,
    "post_id": 1,
    "user_id": 1,
    "created_at": "2021-01-01T00:00:00+00:00"
}

# Sample post data
sample_post = {
    "title": "Test Post",
    "content": "This is a test post",
    "user_id": 1,
    "post_type": "text"
}

sample_post_response = {
    "id": 1,
    "title": "Test Post",
    "content": "This is a test post",
    "user_id": 1,
    "created_at": "2021-01-01T00:00:00+00:00",
    "post_type": "text",
    "kudos_list": [sample_kudos_response]
}




# Test for creating a post
@patch("routers.posts.create_post", return_value=sample_post_response)
@patch("routers.posts.check_user_exists", return_value=True)
def test_create_post_route(create_post, check_user_exists):
    response = client.post("/posts/", json=sample_post)
    assert response.status_code == 200
    assert response.json()["message"] == "Post created successfully"
    
# Test for creating a post with non-existent user
@patch("routers.posts.check_user_exists", return_value=False)
def test_create_post_route_user_not_found(check_user_exists):
    response = client.post("/posts/", json=sample_post)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found with ID 1"
    
# Test for creating a post - not created
@patch("routers.posts.check_user_exists", return_value=True)
@patch("routers.posts.create_post", return_value=None)
def test_create_post_route_not_created(check_user_exists, create_post):
    response = client.post("/posts/", json=sample_post)
    assert response.status_code == 500
    assert "An error occurred while creating the post" in response.json()["detail"]

# Test for getting posts by user ID
@patch("routers.posts.get_posts_by_user_id", return_value=[sample_post_response])
@patch("routers.posts.check_user_exists", return_value=True)
def test_get_posts_by_user_id_route(get_posts_by_user_id, check_user_exists):
    response = client.get("/posts/user/1")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["content"] == "This is a test post"
    assert response.json()["data"][0]["user_id"] == 1
    
# Test for getting posts by user ID - user not found
@patch("routers.posts.check_user_exists", return_value=False)
def test_get_posts_by_user_id_route_user_not_found(check_user_exists):
    response = client.get("/posts/user/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found with ID 1"
    
# Test for getting posts by user ID - not found
@patch("routers.posts.check_user_exists", return_value=True)
@patch("routers.posts.get_posts_by_user_id", return_value=None)
def test_get_posts_by_user_id_route_not_found(check_user_exists, get_posts_by_user_id):
    response = client.get("/posts/user/1")
    assert response.status_code == 500
    assert "An error occurred while retrieving the posts" in response.json()["detail"]

# Test for deleting a post
@patch("routers.posts.delete_post", return_value=True)
@patch("services.post.check_post_exists", return_value=True)
def test_delete_post_route(delete_post, check_post_exists):
    response = client.delete("/posts/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Post deleted successfully"
    
# Test for deleting a post - not found
@patch("services.post.check_post_exists", return_value=False)
def test_delete_post_route_not_found(delete_post):
    response = client.delete("/posts/1")
    assert response.status_code == 500
    assert "An error occurred while deleting the post" in response.json()["detail"]

# Test for adding kudos to a post
@patch("routers.posts.add_kudos", return_value=sample_kudos_response)
@patch("services.post.check_post_exists", return_value=True)
@patch("routers.posts.check_user_exists", return_value=True)
def test_add_kudos_route(add_kudos, check_post_exists, check_user_exists):
    response = client.post("/posts/1/kudos", json=sample_kudos)
    assert response.status_code == 200
    assert response.json()["message"] == "Kudos added successfully"
    
# Test for adding kudos to a post - user not found
@patch("routers.posts.check_user_exists", return_value=False)
def test_add_kudos_route_user_not_found(check_user_exists):
    response = client.post("/posts/1/kudos", json=sample_kudos)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found with ID 1"
    
# Test for adding kudos to a post - not found
@patch("routers.posts.check_user_exists", return_value=True)
@patch("services.post.check_kudos_exists", return_value=False)
def test_add_kudos_route_not_added(check_user_exists, check_kudos_exists):
    response = client.post("/posts/1/kudos", json=sample_kudos)
    assert response.status_code == 500
    assert "An error occurred while adding kudos" in response.json()["detail"]

# Test for getting kudos by post ID
@patch("routers.posts.get_kudos_by_post_id", return_value=[sample_kudos_response])
@patch("services.post.check_post_exists", return_value=True)
def test_get_kudos_by_post_id_route(get_kudos_by_post_id, check_post_exists):
    response = client.get("/posts/1/kudos")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["post_id"] == 1
    assert response.json()["data"][0]["user_id"] == 1
    
# Test for getting kudos by post ID - not found
@patch("services.post.check_post_exists", return_value=True)
@patch("routers.posts.get_kudos_by_post_id", return_value=None)
def test_get_kudos_by_post_id_route_not_found(check_post_exists, get_kudos_by_post_id):
    response = client.get("/posts/1/kudos")
    assert response.status_code == 500
    assert "An error occurred while retrieving the kudos" in response.json()["detail"]

# Test for deleting kudos
@patch("routers.posts.delete_kudos", return_value=True)
@patch("services.post.check_post_exists", return_value=True)
@patch("routers.posts.check_user_exists", return_value=True)
@patch("services.post.check_kudos_exists", return_value=True)
def test_delete_kudos_route(delete_kudos, check_post_exists, check_user_exists, check_kudos_exists):
    response = client.delete("/posts/1/kudos/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Kudos deleted successfully"
    
# Test for deleting kudos - user not found
@patch("routers.posts.check_user_exists", return_value=False)
def test_delete_kudos_route_user_not_found(check_user_exists):
    response = client.delete("/posts/1/kudos/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found with ID 1"
    
# Test for deleting kudos - kudos not found
@patch("routers.posts.check_user_exists", return_value=True)
@patch("services.post.check_kudos_exists", return_value=False)
def test_delete_kudos_route_not_found(check_user_exists, delete_kudos):
    response = client.delete("/posts/1/kudos/1")
    assert response.status_code == 500
    assert "An error occurred while deleting the kudos" in response.json()["detail"]

# Test for getting friends' posts
@patch("routers.posts.get_friends_posts", return_value=[sample_post_response])
@patch("routers.posts.check_user_exists", return_value=True)
def test_get_friends_posts_route(get_friends_posts, check_user_exists):
    response = client.get("/posts/friends/1")
    assert response.status_code == 200
    assert response.json()["data"][0]["content"] == "This is a test post"
    assert response.json()["data"][0]["user_id"] == 1
    
# Test for getting friends' posts - user not found
@patch("routers.posts.check_user_exists", return_value=False)
def test_get_friends_posts_route_user_not_found(check_user_exists):
    response = client.get("/posts/friends/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found with ID 1"
    
# Test for getting friends' posts - not found
@patch("routers.posts.check_user_exists", return_value=True)
@patch("routers.posts.get_friends_posts", return_value=None)
def test_get_friends_posts_route_not_found(check_user_exists, get_friends_posts):
    response = client.get("/posts/friends/1")
    assert response.status_code == 500
    assert "An error occurred while retrieving the friends' posts" in response.json()["detail"]