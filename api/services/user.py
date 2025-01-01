from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from models.user import User
from models.friend import Friend
from models.enums import FriendshipStatus
from schemas.user import UserCreate, UserUpdate

import logging
logger = logging.getLogger(__name__)

def check_user_exists(db: Session, user_id: int) -> bool:
    logger.info(f"Checking if user exists with ID: {user_id}")
    user = db.query(User).filter(User.id == user_id).first()
    return user is not None

def check_user_exists_by_username(db: Session, username: str) -> bool:
    logger.info(f"Checking if user exists with username: {username}")
    user = db.query(User).filter(User.username == username).first()
    return user is not None

def check_user_exists_by_email(db: Session, email: str) -> bool:
    logger.info(f"Checking if user exists with email: {email}")
    user = db.query(User).filter(User.email == email).first()
    return user is not None

def create_user(db: Session, user: UserCreate) -> User:
    logger.info(f"Creating user with email: {user.email}")
    try:
        if check_user_exists_by_username(db, user.username):
            raise HTTPException(status_code=400, detail=f"Username '{user.username}' is already in use.")
        if check_user_exists_by_email(db, user.email):
            raise HTTPException(status_code=400, detail=f"Email '{user.email}' is already in use.")
        
        new_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            email=user.email,
            password=user.password,
            birthdate=user.birthdate,
            city=user.city,
            current_points=user.current_points,
            total_points=user.total_points,
            role=user.role,
            created_at=datetime.now(tz=timezone.utc),
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while creating the user.") from e

def get_user_by_id(db: Session, user_id: int) -> User:
    logger.info(f"Retrieving user with ID: {user_id}")
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail=f"User not found with ID {user_id}")
        return user
    except SQLAlchemyError as e:
        logger.error(f"An error occurred while retrieving the user by ID {user_id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the user.") from e

def get_user_by_email_and_password(db: Session, email: str, password: str) -> User:
    logger.info(f"Retrieving user with email: {email}")
    try:
        user = db.query(User).filter(User.email == email, User.password == password).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found with email and password combination")
        return user
    except SQLAlchemyError as e:
        logger.error(f"An error occurred while retrieving the user by email {email}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the user.") from e

def get_users_by_partial_username(db: Session, username: str) -> list[User]:
    logger.info(f"Retrieving users with partial username: {username}")
    try:
        users = db.query(User).filter(User.username.contains(username)).all()
        if not users:
            raise HTTPException(status_code=404, detail=f"Users not found with partial username {username}")
        return users
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving users.") from e

def update_user(db: Session, user_id: int, user_partial: UserUpdate) -> User:
    logger.info(f"Updating user with ID: {user_id}")
    try:
        if not check_user_exists(db, user_id):
            raise HTTPException(status_code=404, detail=f"User not found with ID {user_id}")
        user = get_user_by_id(db, user_id)
        user_data = user_partial.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while updating the user.") from e

def delete_user(db: Session, user_id: int) -> None:
    logger.info(f"Deleting user with ID: {user_id}")
    try:
        user = get_user_by_id(db, user_id)
        db.delete(user)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while deleting the user.") from e

def send_friend_request(db: Session, user_id: int, friend_id: int) -> Friend:
    logger.info(f"Sending friend request from user {user_id} to user {friend_id}")
    try:
        if not check_user_exists(db, friend_id):
            raise HTTPException(status_code=404, detail=f"User not found with ID {friend_id}")
        new_friend = Friend(sender_id=user_id, receiver_id=friend_id)
        db.add(new_friend)
        db.commit()
        db.refresh(new_friend)
        return new_friend
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while sending the friend request.") from e

def edit_friend_request(db: Session, user_id: int, friend_id: int, status: FriendshipStatus) -> Friend:
    logger.info(f"Editing friend request from user {user_id} to user {friend_id} with status {status}")
    try:
        request = db.query(Friend).filter(Friend.sender_id == user_id, Friend.receiver_id == friend_id).first()
        if not request:
            raise HTTPException(status_code=404, detail=f"Friend request not found with IDs {user_id} and {friend_id}")
        request.status = status
        db.commit()
        db.refresh(request)
        return request
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while updating the friend request.") from e

def get_friends(db: Session, user_id: int) -> list[User]:
    logger.info(f"Retrieving friends for user with ID: {user_id}")
    try:
        friends = db.query(Friend).filter(
            or_(Friend.sender_id == user_id, Friend.receiver_id == user_id),
            Friend.status == FriendshipStatus.ACCEPTED
        ).all()
        if not friends:
            raise HTTPException(status_code=404, detail=f"Friends not found for user with ID {user_id}")
        output = list()
        for friend in friends:
            if friend.sender_id == user_id:
                output.append(friend.receiver)
            else:
                output.append(friend.sender)
        return output
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving friends.") from e

def get_friend_requests(db: Session, user_id: int) -> list[Friend]:
    logger.info(f"Retrieving friend requests for user with ID: {user_id}")
    try:
        requests = db.query(Friend).filter(Friend.receiver_id == user_id, Friend.status == FriendshipStatus.PENDING).all()
        if not requests:
            raise HTTPException(status_code=404, detail=f"Friend requests not found for user with ID {user_id}")
        return requests
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving friend requests.") from e

def get_sent_requests(db: Session, user_id: int) -> list[Friend]:
    logger.info(f"Retrieving sent requests for user with ID: {user_id}")
    try:
        requests = db.query(Friend).filter(Friend.sender_id == user_id, Friend.status == FriendshipStatus.PENDING).all()
        if not requests:
            raise HTTPException(status_code=404, detail=f"Sent requests not found for user with ID {user_id}")
        return requests
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving sent requests.") from e

def delete_friend(db: Session, user_id: int, friend_id: int) -> None:
    logger.info(f"Deleting friend with ID {friend_id} for user with ID {user_id}")
    try:
        friend = db.query(Friend).filter(Friend.sender_id == user_id, Friend.receiver_id == friend_id).first()
        if not friend:
            raise HTTPException(status_code=404, detail=f"Friend not found with IDs {user_id} and {friend_id}")
        db.delete(friend)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while deleting the friend.") from e