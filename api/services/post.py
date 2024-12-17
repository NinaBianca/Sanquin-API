from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from models.post import Post
from models.kudos import Kudos
from schemas.post import PostResponse, KudosResponse

def check_post_exists(db, post_id):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return False
    return True

def create_post(db: Session, post: PostResponse):
    new_post = PostResponse(
        content=post.content,
        user_id=post.user_id,
        created_at=datetime.now(tz=timezone.utc),
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    if not new_post:
        raise HTTPException(
            status_code=400, detail="Post could not be created"
        )
    return new_post

def get_posts_by_user_id(db: Session, user_id: int):
    posts = db.query(Post).filter(Post.user_id == user_id).all()
    if not posts:
        raise HTTPException(
            status_code=404, detail=f"No posts found for user with ID {user_id}"
        )
    
    for post in posts:
        post = PostResponse(
            id=post.id,
            content=post.content,
            user_id=post.user_id,
            created_at=post.created_at,
        )
        
    return posts

def delete_post(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=404, detail=f"Post not found with ID {post_id}"
        )
    db.delete(post)
    db.commit()
    return post

def check_kudos_exists(db: Session, post_id: int, user_id: int):
    kudos = db.query(Kudos).filter(Kudos.post_id == post_id, Kudos.user_id == user_id).first()
    if not kudos:
        return False
    return True

def add_kudos(db: Session, kudos: Kudos):
    new_kudos = KudosResponse(
        post_id=kudos.post_id,
        user_id=kudos.user_id,
        time_created=datetime.now(tz=timezone.utc),
    )
    db.add(new_kudos)
    db.commit()
    db.refresh(new_kudos)
    if not new_kudos:
        raise HTTPException(
            status_code=400, detail="Kudos could not be created"
        )
    return new_kudos

def get_kudos_by_post_id(db: Session, post_id: int):
    kudos = db.query(Kudos).filter(Kudos.post_id == post_id).all()
    if not kudos:
        raise HTTPException(
            status_code=404, detail=f"No kudos found for post with ID {post_id}"
        )
    for kudo in kudos:
        kudo = KudosResponse(
            post_id=kudo.post_id,
            user_id=kudo.user_id,
            time_created=kudo.created_at,
        )
    return kudos

def delete_kudos(db: Session, post_id: int, user_id: int):
    kudos = db.query(Kudos).filter(Kudos.post_id == post_id, Kudos.user_id == user_id).first()
    if not kudos:
        raise HTTPException(
            status_code=404, detail=f"Kudos not found for post with ID {post_id} and user with ID {user_id}"
        )
    db.delete(kudos)
    db.commit()
    return kudos

def get_friends_posts(db: Session, user_id: list[int], limit: int, offset: int):
    posts = db.query(Post).filter(Post.user_id.in_(user_id)).order_by(desc(Post.time_created)).limit(limit).offset(offset).all()
    if not posts:
        raise HTTPException(
            status_code=404, detail=f"No posts found for friends"
        )
    for post in posts:
        post = PostResponse(
            id=post.id,
            content=post.content,
            user_id=post.user_id,
            created_at=post.created_at,
        )
    return posts