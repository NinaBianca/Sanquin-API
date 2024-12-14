from fastapi import APIRouter, Depends, HTTPException
from models.user import User
from models.enums import FriendshipStatus
from schemas.response import ResponseModel
from schemas.user import UserCollection, UserModel, UpdateUserModel
from sqlalchemy.orm import Session
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
    check_user_exists_by_username,
    get_user_by_email_and_password
)
from database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

    


@router.post("/", response_model=ResponseModel)
def create_user_route(user: UserModel, db: Session = Depends(get_db)):
    if check_user_exists_by_username(db, user.username):
        raise HTTPException(status_code=400, detail=f"Username '{user.username}' is already in use.")
    
    new_user = create_user(db, user).model_dump()
    return ResponseModel(status=200, data=new_user, message="User created successfully")


@router.get("/{user_id}", response_model=ResponseModel)
def get_user_by_id_route(user_id: int, db: Session = Depends(get_db)):
    if not check_user_exists(db, user_id):
        raise HTTPException(status_code=404, detail=f"User not found with ID {user_id}")
    user = get_user_by_id(db, user_id).model_dump()
    return ResponseModel(status=200, data=user, message="User retrieved successfully")


@router.get("/email/{email}", response_model=ResponseModel)
def get_user_by_email_and_password_route(email: str, password: str, db: Session = Depends(get_db)):
    user = get_user_by_email_and_password(db, email, password).model_dump()
    return ResponseModel(status=200, data=user, message="User retrieved successfully")


@router.get("/username/{username}", response_model=ResponseModel)
def get_users_by_partial_username_route(username: str, db: Session = Depends(get_db)):
    users = get_users_by_partial_username(db, username)
    users = [user.model_dump() for user in users]
    return ResponseModel(status=200, data=users, message="Users retrieved successfully")


@router.put("/{user_id}", response_model=ResponseModel)
def update_user_route(user_id: int, user: UpdateUserModel, db: Session = Depends(get_db)):
    if not check_user_exists(db, user_id):
        raise HTTPException(status_code=404, detail=f"User not found with ID {user_id}")
    updated_user = update_user(db, user_id, user).model_dump()
    return ResponseModel(status=200, data=updated_user, message="User updated successfully")


@router.delete("/{user_id}", response_model=ResponseModel)
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    if not check_user_exists(db, user_id):
        raise HTTPException(status_code=404, detail=f"User not found with ID {user_id}")
    delete_user(db, user_id)
    return ResponseModel(status=200, data=None, message=f"User with ID {user_id} has been deleted")


@router.post("/{user_id}/friends/{friend_id}", response_model=ResponseModel)
def send_friend_request_route(user_id: int, friend_id: int, db: Session = Depends(get_db)):
    if not check_user_exists(db, friend_id) or not check_user_exists(db, user_id):
        raise HTTPException(status_code=404, detail=f"User not found with ID {friend_id}")
    friend_request = send_friend_request(db, user_id, friend_id)
    return ResponseModel(status=200, data=friend_request, message="Friend request sent successfully")


@router.put("/{user_id}/friends/{friend_id}", response_model=ResponseModel)
def edit_friend_request_route(user_id: int, friend_id: int, status: FriendshipStatus, db: Session = Depends(get_db)):
    if not check_user_exists(db, friend_id) or not check_user_exists(db, user_id):
        raise HTTPException(status_code=404, detail=f"User not found with ID {friend_id}")
    updated_request = edit_friend_request(db, user_id, friend_id, status)
    return ResponseModel(status=200, data=updated_request, message="Friend request updated successfully")


@router.get("/{user_id}/friends", response_model=ResponseModel)
def get_friends_route(user_id: int, db: Session = Depends(get_db)):
    if not check_user_exists(db, user_id):
        raise HTTPException(status_code=404, detail=f"User not found with ID {user_id}")
    friends = get_friends(db, user_id)
    return ResponseModel(status=200, data=friends, message="Friends retrieved successfully")


@router.get("/{user_id}/friend-requests", response_model=ResponseModel)
def get_friend_requests_route(user_id: int, db: Session = Depends(get_db)):
    if not check_user_exists(db, user_id):
        raise HTTPException(status_code=404, detail=f"User not found with ID {user_id}")
    friend_requests = get_friend_requests(db, user_id)
    return ResponseModel(status=200, data=friend_requests, message="Friend requests retrieved successfully")


@router.get("/{user_id}/sent-requests", response_model=ResponseModel)
def get_sent_requests_route(user_id: int, db: Session = Depends(get_db)):
    if not check_user_exists(db, user_id):
        raise HTTPException(status_code=404, detail=f"User not found with ID {user_id}")
    sent_requests = get_sent_requests(db, user_id)
    return ResponseModel(status=200, data=sent_requests, message="Sent requests retrieved successfully")


@router.delete("/{user_id}/friends/{friend_id}", response_model=ResponseModel)
def delete_friend_route(user_id: int, friend_id: int, db: Session = Depends(get_db)):
    if not check_user_exists(db, user_id) or not check_user_exists(db, friend_id):
        raise HTTPException(status_code=404, detail=f"User not found with ID {friend_id}")
    delete_friend(db, user_id, friend_id)
    return ResponseModel(status=200, data=None, message=f"Friend with ID {friend_id} has been removed")
