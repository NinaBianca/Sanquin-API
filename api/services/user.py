from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models.user import User
from ..models.friend import Friend
from ..models.enums import FriendshipStatus

def check_user_exists(db, user_id):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    return True

def create_user(db: Session, user: User):
    new_user = User(
        username=user.username,
        password=user.password,
        email=user.email,
        birthdate=user.birthdate,
        city=user.city,
        points=user.points,
        role=user.role,
        created_at=datetime.now(tz=timezone.utc),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User not found with ID {user_id}")
    return user


def get_user_by_username(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User not found with username {username}")
    return user


def update_user(db: Session, user_id: int, user_partial):
    user = get_user_by_id(db, user_id)  # Reuse existing function for consistency
    user_data = user_partial.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    db.delete(user)
    db.commit()


def send_friend_request(db: Session, user_id: int, friend_id: int):
    new_friend = Friend(sender_id=user_id, receiver_id=friend_id)
    db.add(new_friend)
    db.commit()
    db.refresh(new_friend)
    return new_friend


def edit_friend_request(db: Session, user_id: int, friend_id: int, status: FriendshipStatus):
    request = db.query(Friend).filter(Friend.sender_id == user_id, Friend.receiver_id == friend_id).first()
    if not request:
        raise HTTPException(status_code=404, detail=f"Friend request not found with IDs {user_id} and {friend_id}")
    request.status = status
    db.commit()
    db.refresh(request)
    return request


def get_friends(db: Session, user_id: int):
    friends = db.query(Friend).filter(Friend.sender_id == user_id, Friend.status == "ACCEPTED").all()
    if not friends:
        raise HTTPException(status_code=404, detail=f"Friends not found for user with ID {user_id}")
    return friends


def get_friend_requests(db: Session, user_id: int):
    requests = db.query(Friend).filter(Friend.receiver_id == user_id, Friend.status == "PENDING").all()
    if not requests:
        raise HTTPException(status_code=404, detail=f"Friend requests not found for user with ID {user_id}")
    return requests


def get_sent_requests(db: Session, user_id: int):
    requests = db.query(Friend).filter(Friend.sender_id == user_id, Friend.status == "PENDING").all()
    if not requests:
        raise HTTPException(status_code=404, detail=f"Sent requests not found for user with ID {user_id}")
    return requests


def delete_friend(db: Session, user_id: int, friend_id: int):
    friend = db.query(Friend).filter(Friend.sender_id == user_id, Friend.receiver_id == friend_id).first()
    if not friend:
        raise HTTPException(status_code=404, detail=f"Friend not found with IDs {user_id} and {friend_id}")
    db.delete(friend)
    db.commit()
