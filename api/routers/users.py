from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.enums import FriendshipStatus
from schemas.response import ResponseModel
from schemas.user import UserCreate, UserUpdate, UserResponse
from services.user import (
    create_user,
    get_user_by_id,
    get_users_by_partial_username,
    update_user,
    delete_user,
    send_friend_request,
    edit_friend_request,
    get_friends,
    get_friend_requests,
    get_sent_requests,
    delete_friend,
    check_user_exists,
    get_user_by_email_and_password
)
from database import get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/", response_model=ResponseModel)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = create_user(db, user)
        return ResponseModel(status=200, data=UserResponse.model_validate(new_user), message="User created successfully")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while creating the user.") from e

@router.get("/id/{user_id}", response_model=ResponseModel)
def get_user_by_id_route(user_id: int, db: Session = Depends(get_db)):
    try:
        user = get_user_by_id(db, user_id)
        return ResponseModel(status=200, data=UserResponse.model_validate(user), message="User retrieved successfully")
    except HTTPException as e:
        logger.error(f"An error occurred while retrieving the user: {e}")
        raise e
    except Exception as e:
        logger.error(f"An error occurred while retrieving the user: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the user.") from e

@router.get("/email/{email}", response_model=ResponseModel)
def get_user_by_email_and_password_route(email: str, password: str, db: Session = Depends(get_db)):
    try:
        user = get_user_by_email_and_password(db, email, password)
        return ResponseModel(status=200, data=UserResponse.model_validate(user), message="User retrieved successfully")
    except HTTPException as e:
        logger.error(f"An error occurred while retrieving the user by email and password: {e}")
        raise e
    except Exception as e:
        logger.error(f"An error occurred while retrieving the user by email and password: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the user.") from e

@router.get("/username/{username}", response_model=ResponseModel)
def get_users_by_partial_username_route(username: str, db: Session = Depends(get_db)):
    try:
        users = get_users_by_partial_username(db, username)
        return ResponseModel(status=200, data=[UserResponse.model_validate(user) for user in users], message="Users retrieved successfully")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving users.") from e

@router.put("/update/{user_id}", response_model=ResponseModel)
def update_user_route(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    try:
        updated_user = update_user(db, user_id, user)
        return ResponseModel(status=200, data=UserResponse.model_validate(updated_user), message="User updated successfully")
    except HTTPException as e:
        logger.error(f"An error occurred while updating the user: {e}")
        raise e
    except Exception as e:
        logger.error(f"An error occurred while updating the user: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the user.") from e

@router.delete("/{user_id}", response_model=ResponseModel)
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    try:
        delete_user(db, user_id)
        return ResponseModel(status=200, data=None, message=f"User with ID {user_id} has been deleted")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while deleting the user.") from e

@router.post("/{user_id}/friends/{friend_id}", response_model=ResponseModel)
def send_friend_request_route(user_id: int, friend_id: int, db: Session = Depends(get_db)):
    try:
        friend_request = send_friend_request(db, user_id, friend_id)
        return ResponseModel(status=200, data=friend_request, message="Friend request sent successfully")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while sending the friend request.") from e

@router.put("/{user_id}/friends/{friend_id}", response_model=ResponseModel)
def edit_friend_request_route(user_id: int, friend_id: int, status: FriendshipStatus, db: Session = Depends(get_db)):
    try:
        print(f"User {user_id} is updating friend request with user {friend_id} to status {status}")
        logger.info(f"User {user_id} is updating friend request with user {friend_id} to status {status}")
        updated_request = edit_friend_request(db, user_id, friend_id, status)
        return ResponseModel(status=200, data=updated_request, message="Friend request updated successfully")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"An error occurred: {e}")
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the friend request.") from e

@router.get("/{user_id}/friends", response_model=ResponseModel)
def get_friends_route(user_id: int, db: Session = Depends(get_db)):
    try:
        friends = get_friends(db, user_id)
        return ResponseModel(status=200, data=friends, message="Friends retrieved successfully")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving friends.") from e

@router.get("/{user_id}/friend-requests", response_model=ResponseModel)
def get_friend_requests_route(user_id: int, db: Session = Depends(get_db)):
    try:
        friend_requests = get_friend_requests(db, user_id)
        return ResponseModel(status=200, data=friend_requests, message="Friend requests retrieved successfully")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving friend requests.") from e

@router.get("/{user_id}/sent-requests", response_model=ResponseModel)
def get_sent_requests_route(user_id: int, db: Session = Depends(get_db)):
    try:
        sent_requests = get_sent_requests(db, user_id)
        return ResponseModel(status=200, data=sent_requests, message="Sent requests retrieved successfully")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving sent requests.") from e

@router.delete("/{user_id}/friends/{friend_id}", response_model=ResponseModel)
def delete_friend_route(user_id: int, friend_id: int, db: Session = Depends(get_db)):
    try:
        delete_friend(db, user_id, friend_id)
        return ResponseModel(status=200, data=None, message=f"Friend with ID {friend_id} has been removed")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while deleting the friend.") from e
    
