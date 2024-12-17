from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.response import ResponseModel
from ..schemas.challenge import ChallengeCreate, ChallengeBase
from ..services.challenge import (
    check_challenge_exists,
    create_challenge,
    get_challenges,
    get_challenges_by_user_id,
    delete_challenge,
    update_challenge,
    get_challenge_by_id
)
from ..services.user import check_user_exists

router = APIRouter(
    prefix="/challenges",
    tags=["challenges"],
)

@router.post("/", response_model=ResponseModel)
def create_new_challenge(challenge: ChallengeCreate, db: Session = Depends(get_db)):
    new_challenge = create_challenge(db=db, challenge=challenge)
    return ResponseModel(status=200, data=new_challenge, message="Challenge created successfully")

@router.get("/", response_model=ResponseModel)
def read_challenges(db: Session = Depends(get_db)):
    challenges = get_challenges(db=db)
    return ResponseModel(status=200, data=challenges, message="Challenges retrieved successfully")

@router.get("/{challenge_id}", response_model=ResponseModel)
def get_challenge(challenge_id: int, db: Session = Depends(get_db)):
    if not check_challenge_exists(db, challenge_id):
        raise HTTPException(status_code=404, detail=f"Challenge not found with ID {challenge_id}")
    challenge = get_challenge_by_id(db, challenge_id)
    return ResponseModel(status=200, data=challenge, message="Challenge retrieved successfully")

@router.put("/{challenge_id}", response_model=ResponseModel)
def update_challenge_route(challenge_id: int, challenge: ChallengeBase, db: Session = Depends(get_db)):
    if not check_challenge_exists(db, challenge_id):
        raise HTTPException(status_code=404, detail=f"Challenge not found with ID {challenge_id}")
    updated_challenge = update_challenge(db, challenge_id, challenge)
    return ResponseModel(status=200, data=updated_challenge, message="Challenge updated successfully")

@router.delete("/{challenge_id}", response_model=ResponseModel)
def remove_challenge(challenge_id: int, db: Session = Depends(get_db)):
    if not check_challenge_exists(db, challenge_id):
        raise HTTPException(status_code=404, detail=f"Challenge not found with ID {challenge_id}")
    delete_challenge(db=db, challenge_id=challenge_id)
    return ResponseModel(status=200, message="Challenge deleted successfully")

@router.post("/{challenge_id}/user/{user_id}", response_model=ResponseModel)
def add_user_to_challenge(user_id: int, challenge_id: int, db: Session = Depends(get_db)):
    if not check_user_exists(db, user_id):
        raise HTTPException(status_code=404, detail=f"User not found with ID {user_id}")
    if not check_challenge_exists(db, challenge_id):
        raise HTTPException(status_code=404, detail=f"Challenge not found with ID {challenge_id}")
    add_user_to_challenge(db, user_id, challenge_id)
    return ResponseModel(status=200, message="User added to challenge successfully")

@router.get("/user/{user_id}", response_model=ResponseModel)
def read_challenges_by_user_id(user_id: int, db: Session = Depends(get_db)):
    if not check_user_exists(db, user_id):
        raise HTTPException(status_code=404, detail=f"User not found with ID {user_id}")
    challenges = get_challenges_by_user_id(db=db, user_id=user_id)
    return ResponseModel(status=200, data=challenges, message="Challenges retrieved successfully")

@router.get("/{challenge_id}/users", response_model=ResponseModel)
def get_users_by_challenge_id(challenge_id: int, db: Session = Depends(get_db)):
    if not check_challenge_exists(db, challenge_id):
        raise HTTPException(status_code=404, detail=f"Challenge not found with ID {challenge_id}")
    users = get_users_by_challenge_id(db, challenge_id)
    return ResponseModel(status=200, data=users, message="Users retrieved successfully")

@router.delete("/{challenge_id}/user/{user_id}", response_model=ResponseModel)
def delete_user_from_challenge(user_id: int, challenge_id: int, db: Session = Depends(get_db)):
    if not check_user_exists(db, user_id):
        raise HTTPException(status_code=404, detail=f"User not found with ID {user_id}")
    if not check_challenge_exists(db, challenge_id):
        raise HTTPException(status_code=404, detail=f"Challenge not found with ID {challenge_id}")
    delete_user_from_challenge(db, user_id, challenge_id)
    return ResponseModel(status=200, message="User deleted from challenge successfully")
