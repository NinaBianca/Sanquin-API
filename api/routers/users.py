from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.enums import FriendshipStatus
from schemas.response import ResponseModel
from schemas.user import UserCreate, UserUpdate, UserResponse
from schemas.friend import FriendRequestModel
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
    get_user_by_email_and_password,
    create_notification,
    get_notifications,
    get_new_notifications
)
from database import get_db
from schemas.notification import NotificationCreate, NotificationResponse


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/", response_model=ResponseModel)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = create_user(db, user)
        return ResponseModel(status=200, data=UserResponse.model_validate(new_user), message="User created successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the user: {e}.") from e

@router.get("/id/{user_id}", response_model=ResponseModel)
def get_user_by_id_route(user_id: int, db: Session = Depends(get_db)):
    try:
        user = get_user_by_id(db, user_id)
        return ResponseModel(status=200, data=UserResponse.model_validate(user), message="User retrieved successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving the user: {e}") from e

@router.get("/email/{email}", response_model=ResponseModel)
def get_user_by_email_and_password_route(email: str, password: str, db: Session = Depends(get_db)):
    try:
        user = get_user_by_email_and_password(db, email, password)
        return ResponseModel(status=200, data=UserResponse.model_validate(user), message="User retrieved successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving the user: {e}") from e

@router.get("/username/{username}", response_model=ResponseModel)
def get_users_by_partial_username_route(username: str, db: Session = Depends(get_db)):
    try:
        users = get_users_by_partial_username(db, username)
        return ResponseModel(status=200, data=[UserResponse.model_validate(user) for user in users], message="Users retrieved successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving users: {e}") from e

@router.put("/update/{user_id}", response_model=ResponseModel)
def update_user_route(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    try:
        updated_user = update_user(db, user_id, user)
        return ResponseModel(status=200, data=UserResponse.model_validate(updated_user), message="User updated successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the user: {e}") from e

@router.delete("/{user_id}", response_model=ResponseModel)
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    try:
        delete_user(db, user_id)
        return ResponseModel(status=200, data=None, message=f"User with ID {user_id} has been deleted")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while deleting the user: {e}") from e

@router.post("/{user_id}/friends/{friend_id}", response_model=ResponseModel)
def send_friend_request_route(user_id: int, friend_id: int, db: Session = Depends(get_db)):
    try:
        friend_request = send_friend_request(db, user_id, friend_id)
        return ResponseModel(status=200, data=FriendRequestModel.model_validate(friend_request), message="Friend request sent successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while sending the friend request: {e}") from e

@router.put("/{user_id}/friends/{friend_id}", response_model=ResponseModel)
def edit_friend_request_route(user_id: int, friend_id: int, status: FriendshipStatus, db: Session = Depends(get_db)):
    try:
        updated_request = edit_friend_request(db, user_id, friend_id, status)
        return ResponseModel(status=200, data=FriendRequestModel.model_validate(updated_request), message="Friend request updated successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the friend request: {e}") from e

@router.get("/{user_id}/friends", response_model=ResponseModel)
def get_friends_route(user_id: int, db: Session = Depends(get_db)):
    try:
        friends = get_friends(db, user_id)
        output = [UserResponse.model_validate(friend) for friend in friends]
        return ResponseModel(status=200, data=output, message="Friends retrieved successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving friends: {e}") from e

@router.get("/{user_id}/friend-requests", response_model=ResponseModel)
def get_friend_requests_route(user_id: int, db: Session = Depends(get_db)):
    try:
        friend_requests = get_friend_requests(db, user_id)
        output = [FriendRequestModel.model_validate(request) for request in friend_requests]
        return ResponseModel(status=200, data=output, message="Friend requests retrieved successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving friend requests: {e}") from e

@router.get("/{user_id}/sent-requests", response_model=ResponseModel)
def get_sent_requests_route(user_id: int, db: Session = Depends(get_db)):
    try:
        sent_requests = get_sent_requests(db, user_id)
        output = [FriendRequestModel.model_validate(request) for request in sent_requests]
        return ResponseModel(status=200, data=output, message="Sent requests retrieved successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving sent requests: {e}") from e

@router.delete("/{user_id}/friends/{friend_id}", response_model=ResponseModel)
def delete_friend_route(user_id: int, friend_id: int, db: Session = Depends(get_db)):
    try:
        delete_friend(db, user_id, friend_id)
        return ResponseModel(status=200, data=None, message=f"Friend with ID {friend_id} has been removed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while deleting the friend: {e}") from e
    
@router.post("/{user_id}/notifications", response_model=ResponseModel)
def create_notification_route(notification: NotificationCreate, db: Session = Depends(get_db)):
    try:
        notification = create_notification(db, notification)
        return ResponseModel(status=200, data=NotificationResponse.model_validate(notification), message="Notification created successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the notification: {e}") from e
    
@router.get("/{user_id}/notifications", response_model=ResponseModel)
def get_notifications_route(user_id: int, db: Session = Depends(get_db)):
    try:
        notifications = get_notifications(db, user_id)
        output = [NotificationResponse.model_validate(notification) for notification in notifications]
        return ResponseModel(status=200, data=output, message="Notifications retrieved successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving notifications: {e}") from e
    
@router.get("/{user_id}/new-notifications", response_model=ResponseModel)
def get_new_notifications_route(user_id: int, db: Session = Depends(get_db)):
    try:
        notifications = get_new_notifications(db, user_id)
        output = [NotificationResponse.model_validate(notification) for notification in notifications]
        return ResponseModel(status=200, data=output, message="New notifications retrieved successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving new notifications: {e}") from e
