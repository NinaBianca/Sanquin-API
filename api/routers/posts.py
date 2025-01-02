from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.post import Post as PostModel
from models.kudos import Kudos as KudosModel
from schemas.response import ResponseModel
from schemas.post import PostCreate, PostResponse, KudosCreate, KudosResponse
from services.post import create_post, get_posts_by_user_id, delete_post, add_kudos, get_kudos_by_post_id, delete_kudos, get_friends_posts, check_post_exists, check_kudos_exists
from services.user import check_user_exists

import logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)

@router.post("/", response_model=ResponseModel)
def create_new_post(post: PostCreate, db: Session = Depends(get_db)):
    if post.user_id:
        if not check_user_exists(db, post.user_id):
            raise HTTPException(status_code=404, detail=f"User not found with ID {post.user_id}")
    try:
        new_post = create_post(db=db, post=post)
        return ResponseModel(status=200, data=PostResponse.model_validate(new_post), message="Post created successfully")
    except Exception as e:
        logger.error(f"Error creating post: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the post.") from e

@router.get("/user/{user_id}", response_model=ResponseModel)
def read_posts_by_user_id(user_id: int, db: Session = Depends(get_db)):
    if not check_user_exists(db, user_id):
        raise HTTPException(status_code=404, detail=f"User not found with ID {user_id}")
    try:
        posts = get_posts_by_user_id(db=db, user_id=user_id)
        output = [PostResponse.model_validate(post) for post in posts]
        return ResponseModel(status=200, data=output, message="Posts retrieved successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the posts.") from e
    
@router.delete("/{post_id}", response_model=ResponseModel)
def remove_post(post_id: int, db: Session = Depends(get_db)):
    try:
        delete_post(db=db, post_id=post_id)
        return ResponseModel(status=200, message="Post deleted successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while deleting the post.") from e
    
@router.post("/{post_id}/kudos", response_model=ResponseModel)
def add_kudos_to_post(post_id: int, kudos: KudosCreate, db: Session = Depends(get_db)):
    kudos.post_id = post_id
    if not check_user_exists(db, kudos.user_id):
        raise HTTPException(status_code=404, detail=f"User not found with ID {kudos.user_id}")
    try:
        add_kudos(db=db, kudos=kudos)
        return ResponseModel(status=200, message="Kudos added successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while adding kudos.") from e
    
@router.get("/{post_id}/kudos", response_model=ResponseModel)
def read_kudos_by_post_id(post_id: int, db: Session = Depends(get_db)):
    try:
        kudos = get_kudos_by_post_id(db=db, post_id=post_id)
        output = [KudosResponse.model_validate(kudo) for kudo in kudos]
        return ResponseModel(status=200, data=output, message="Kudos retrieved successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the kudos.") from e
    
@router.delete("/{post_id}/kudos/{user_id}", response_model=ResponseModel)
def remove_kudos(post_id: int, user_id: int, db: Session = Depends(get_db)):
    if not check_user_exists(db, user_id):
        raise HTTPException(status_code=404, detail=f"User not found with ID {user_id}")
    try:
        delete_kudos(db=db, post_id=post_id, user_id=user_id)
        return ResponseModel(status=200, message="Kudos deleted successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while deleting the kudos.") from e
    
@router.get("/friends/{user_id}", response_model=ResponseModel)
def read_friends_posts(user_id: int, db: Session = Depends(get_db)):
    if not check_user_exists(db, user_id):
        raise HTTPException(status_code=404, detail=f"User not found with ID {user_id}")
    try:
        posts = get_friends_posts(db=db, user_id=user_id)
        output = [PostResponse.model_validate(post) for post in posts]
        return ResponseModel(status=200, data=output, message="Friends' posts retrieved successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the friends' posts.") from e