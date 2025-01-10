from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from models.challenge import Challenge
from models.challenge_user import ChallengeUser
from schemas.challenge import ChallengeCreate, ChallengeUpdate


def check_challenge_exists(db, challenge_id):
    return db.query(Challenge).filter(Challenge.id == challenge_id).first() is not None

def create_challenge(db: Session, challenge: ChallengeCreate):
    try:
        new_challenge = Challenge(
            title=challenge.title,
            description=challenge.description,
            location=challenge.location,
            goal=challenge.goal,
            start=challenge.start,
            end=challenge.end,
        )
        db.add(new_challenge)
        db.commit()
        db.refresh(new_challenge)
        if not new_challenge:
            raise HTTPException(
                status_code=400, detail="Challenge could not be created"
            )
        return new_challenge
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=e) from e

def get_challenges(db: Session):
    try:
        challenges = db.query(Challenge).all()
        if not challenges:
            raise HTTPException(
                status_code=404, detail="No challenges found"
            )
        return challenges
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e

def get_challenge_by_id(db: Session, challenge_id: int):
    try:
        if not check_challenge_exists(db, challenge_id):
            raise HTTPException(
                status_code=404, detail=f"Challenge not found with ID {challenge_id}"
            )
        challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
        if not challenge:
            raise HTTPException(
                status_code=404, detail=f"Challenge not found with ID {challenge_id}"
            )
        return challenge
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e   

def update_challenge(db: Session, challenge_id: int, challenge_partial: ChallengeUpdate):
    try:
        if not check_challenge_exists(db, challenge_id):
            raise HTTPException(
                status_code=404, detail=f"Challenge not found with ID {challenge_id}"
            )
        challenge = get_challenge_by_id(db, challenge_id)
        if not challenge:
            raise HTTPException(
                status_code=404, detail=f"Challenge not found with ID {challenge_id}"
            )
        challenge_data = challenge_partial.dict(exclude_unset=True)
 
        for key, value in challenge_data.items():
            setattr(challenge, key, value)
            
        db.commit()
        db.refresh(challenge)
        return challenge
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=e) from e

def delete_challenge(db: Session, challenge_id: int):
    try:
        if not check_challenge_exists(db, challenge_id):
            raise HTTPException(
                status_code=404, detail=f"Challenge not found with ID {challenge_id}"
            )
        challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
        if not challenge:
            raise HTTPException(
                status_code=404, detail=f"Challenge not found with ID {challenge_id}"
            )
        db.delete(challenge)
        db.commit()
        return challenge
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=e) from e

def add_user_to_challenge(db: Session, challenge_id: int, user_id: int):
    try:
        if not check_challenge_exists(db, challenge_id):
            raise HTTPException(
                status_code=404, detail=f"Challenge not found with ID {challenge_id}"
            )
        new_challenge_user = ChallengeUser(
            challenge_id=challenge_id,
            user_id=user_id,
            status="active",
        )
        db.add(new_challenge_user)
        db.commit()
        db.refresh(new_challenge_user)
        if not new_challenge_user:
            raise HTTPException(
                status_code=400, detail="User could not be added to challenge"
            )
        return new_challenge_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=e) from e

def get_users_by_challenge_id(db: Session, challenge_id: int):
    try:
        if not check_challenge_exists(db, challenge_id):
            raise HTTPException(
                status_code=404, detail=f"Challenge not found with ID {challenge_id}"
            )
        challenge_users = db.query(ChallengeUser).filter(ChallengeUser.challenge_id == challenge_id).all()
        if not challenge_users:
            raise HTTPException(
                status_code=404, detail=f"No users found for challenge with ID {challenge_id}"
            )
        return [challenge_user.user for challenge_user in challenge_users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e

def delete_user_from_challenge(db: Session, challenge_id: int, user_id: int):
    try:
        if not check_challenge_exists(db, challenge_id):
            raise HTTPException(
                status_code=404, detail=f"Challenge not found with ID {challenge_id}"
            )
        challenge_user = db.query(ChallengeUser).filter(ChallengeUser.challenge_id == challenge_id, ChallengeUser.user_id == user_id).first()
        if not challenge_user:
            raise HTTPException(
                status_code=404, detail=f"User not found for challenge with ID {challenge_id}"
            )
        db.delete(challenge_user)
        db.commit()
        return challenge_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=e) from e

def get_challenges_by_user_id(db: Session, user_id: int):
    try:
        challenges = db.query(ChallengeUser).filter(ChallengeUser.user_id == user_id).all()
        if not challenges:
            raise HTTPException(
                status_code=404, detail=f"No challenges found for user with ID {user_id}"
            )
        return [challenge.challenge for challenge in challenges]
    except Exception as e:
        raise HTTPException(status_code=500, detail=e) from e

