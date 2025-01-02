from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from models.post import Post
from models.kudos import Kudos
from schemas.post import PostResponse, KudosResponse, PostCreate

def check_post_exists(db, post_id):
    return db.query(Post).filter(Post.id == post_id).first() is not None   
    

def create_post(db: Session, post: PostCreate):
    try:
        new_post = Post(
            title=post.title,
            content=post.content,
            user_id=post.user_id,
            created_at=datetime.now(tz=timezone.utc),
            post_type=post.post_type,
        )
        print(new_post)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)     
        return new_post
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e
  

def get_posts_by_user_id(db: Session, user_id: int):
    try:
        posts = db.query(Post).filter(Post.user_id == user_id).all()
        if not posts:
            raise HTTPException(
                status_code=404, detail=f"No posts found for user with ID {user_id}"
            )
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e

def delete_post(db: Session, post_id: int):
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not check_post_exists(db, post_id):
            raise HTTPException(
                status_code=404, detail=f"Post not found with ID {post_id}"
            )
        db.delete(post)
        db.commit()
        return post
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e

def check_kudos_exists(db: Session, post_id: int, user_id: int):
    return db.query(Kudos).filter(Kudos.post_id == post_id, Kudos.user_id == user_id).first() is not None


def add_kudos(db: Session, kudos: Kudos):
    try:
        if not check_post_exists(db, kudos.post_id):
            raise HTTPException(
                status_code=404, detail=f"Post not found with ID {kudos.post_id}"
            )
            
        new_kudos = Kudos(
            post_id=kudos.post_id,
            user_id=kudos.user_id,
            created_at=datetime.now(tz=timezone.utc),
        )
        db.add(new_kudos)
        db.commit()
        db.refresh(new_kudos)
        if not new_kudos:
            raise HTTPException(
                status_code=400, detail="Kudos could not be created"
            )
        return new_kudos
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e

def get_kudos_by_post_id(db: Session, post_id: int):
    try:
        if not check_post_exists(db, post_id):
            raise HTTPException(
                status_code=404, detail=f"Post not found with ID {post_id}"
            )
            
        kudos = db.query(Kudos).filter(Kudos.post_id == post_id).all()
        if not kudos:
            raise HTTPException(
                status_code=404, detail=f"No kudos found for post with ID {post_id}"
            )
        return kudos
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e

def delete_kudos(db: Session, post_id: int, user_id: int):
    try:
        if not check_post_exists(db, post_id):
            raise HTTPException(
                status_code=404, detail=f"Post not found with ID {post_id}"
            )
        if not check_kudos_exists(db, post_id, user_id):
            raise HTTPException(
                status_code=404, detail=f"Kudos not found for post with ID {post_id} and user with ID {user_id}"
            )
        kudos = db.query(Kudos).filter(Kudos.post_id == post_id, Kudos.user_id == user_id).first()
        if not kudos:
            raise HTTPException(
                status_code=404, detail=f"Kudos not found for post with ID {post_id} and user with ID {user_id}"
            )
        db.delete(kudos)
        db.commit()
        return kudos
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e

def get_friends_posts(db: Session, user_id: list[int], limit: int = 10 , offset: int = 0):
    try:
        posts = db.query(Post).filter(Post.user_id == user_id).order_by(desc(Post.created_at)).limit(limit).offset(offset).all()
        if not posts:
            raise HTTPException(
                status_code=404, detail=f"No posts found for friends"
            )
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e