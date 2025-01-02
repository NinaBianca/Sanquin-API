from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.response import ResponseModel
from schemas.challenge import ChallengeCreate, ChallengeUpdate, ChallengeResponse
from schemas.user import UserResponse
from services.challenge import (
    create_challenge,
    get_challenges,
    get_challenges_by_user_id,
    delete_challenge,
    update_challenge,
    get_challenge_by_id,
    add_user_to_challenge,
    get_users_by_challenge_id,
    delete_user_from_challenge
)
from services.user import check_user_exists

router = APIRouter(
    prefix="/challenges",
    tags=["challenges"],
)

@router.post("/", response_model=ResponseModel)
def create_new_challenge_route(challenge: ChallengeCreate, db: Session = Depends(get_db)):
    try:
        new_challenge = create_challenge(db=db, challenge=challenge)
        return ResponseModel(status=200, data=ChallengeResponse.model_validate(new_challenge), message="Challenge created successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the challenge: {e}") from e

@router.get("/", response_model=ResponseModel)
def read_challenges_route(db: Session = Depends(get_db)):
    try:
        challenges = get_challenges(db=db)
        return ResponseModel(status=200, data=[ChallengeResponse.model_validate(challenge) for challenge in challenges], message="Challenges retrieved successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving the challenges: {e}") from e

@router.get("/{challenge_id}", response_model=ResponseModel)
def get_challenge_route(challenge_id: int, db: Session = Depends(get_db)):
    try:
        challenge = get_challenge_by_id(db, challenge_id)
        return ResponseModel(status=200, data=ChallengeResponse.model_validate(challenge), message="Challenge retrieved successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving the challenge: {e}") from e

@router.put("/{challenge_id}", response_model=ResponseModel)
def update_challenge_route(challenge_id: int, challenge: ChallengeUpdate, db: Session = Depends(get_db)):
    try:
        updated_challenge = update_challenge(db, challenge_id, challenge)
        return ResponseModel(status=200, data=ChallengeResponse.model_validate(updated_challenge), message="Challenge updated successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the challenge: {e}") from e

@router.delete("/{challenge_id}", response_model=ResponseModel)
def remove_challenge_route(challenge_id: int, db: Session = Depends(get_db)):
    try:
        delete_challenge(db=db, challenge_id=challenge_id)
        return ResponseModel(status=200, message="Challenge deleted successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while deleting the challenge: {e}") from e

@router.post("/{challenge_id}/user/{user_id}", response_model=ResponseModel)
def add_user_to_challenge_route(challenge_id: int, user_id: int, db: Session = Depends(get_db)):
    if not check_user_exists(db, user_id):
            raise HTTPException(status_code=404, detail=f"User not found with ID {user_id}")
    try:
        add_user_to_challenge(db, challenge_id, user_id)
        return ResponseModel(status=200, message="User added to challenge successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while adding user to challenge: {e}") from e

@router.get("/user/{user_id}", response_model=ResponseModel)
def read_challenges_by_user_id_route(user_id: int, db: Session = Depends(get_db)):
    if not check_user_exists(db, user_id):
            raise HTTPException(status_code=404, detail=f"User not found with ID {user_id}")
    try:
        challenges = get_challenges_by_user_id(db=db, user_id=user_id)
        return ResponseModel(status=200, data=[ChallengeResponse.model_validate(challenge) for challenge in challenges], message="Challenges retrieved successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving the challenges: {e}") from e

@router.get("/{challenge_id}/users", response_model=ResponseModel)
def get_users_by_challenge_id_route(challenge_id: int, db: Session = Depends(get_db)):
    try:
        users = get_users_by_challenge_id(db, challenge_id)
        return ResponseModel(status=200, data=[UserResponse.model_validate(user) for user in users], message="Users retrieved successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving the users: {e}") from e

@router.delete("/{challenge_id}/user/{user_id}", response_model=ResponseModel)
def delete_user_from_challenge_route(challenge_id: int, user_id: int, db: Session = Depends(get_db)):
    if not check_user_exists(db, user_id):
            raise HTTPException(status_code=404, detail=f"User not found with ID {user_id}")
    try:
        delete_user_from_challenge(db, challenge_id, user_id)
        return ResponseModel(status=200, message="User deleted from challenge successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while deleting user from challenge: {e}") from e
