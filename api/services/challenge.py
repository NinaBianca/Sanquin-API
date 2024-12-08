from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from models.challenge import Challenge
from models.challenge_user import ChallengeUser

def check_challenge_exists(db, challenge_id):
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        return False
    return True

def create_challenge(db: Session, challenge: Challenge):
    new_challenge = Challenge(
        title=challenge.title,
        description=challenge.description,
        time_created=datetime.now(tz=timezone.utc),
    )
    db.add(new_challenge)
    db.commit()
    db.refresh(new_challenge)
    if not new_challenge:
        raise HTTPException(
            status_code=400, detail="Challenge could not be created"
        )
    return new_challenge

def get_challenges(db: Session):
    challenges = db.query(Challenge).all()
    if not challenges:
        raise HTTPException(
            status_code=404, detail="No challenges found"
        )
    return challenges

def get_challenge_by_id(db: Session, challenge_id: int):
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(
            status_code=404, detail=f"Challenge not found with ID {challenge_id}"
        )
    return challenge

def update_challenge(db: Session, challenge_id: int, challenge_partial):
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(
            status_code=404, detail=f"Challenge not found with ID {challenge_id}"
        )
    challenge_data = challenge_partial.dict(exclude_unset=True)
    for key, value in challenge_data.items():
        setattr(challenge, key, value)
    db.add(challenge)
    db.commit()
    db.refresh(challenge)
    return challenge

def delete_challenge(db: Session, challenge_id: int):
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(
            status_code=404, detail=f"Challenge not found with ID {challenge_id}"
        )
    db.delete(challenge)
    db.commit()
    return challenge

def add_user_to_challenge(db: Session, challenge_user: ChallengeUser):
    new_challenge_user = ChallengeUser(
        challenge_id=challenge_user.challenge_id,
        user_id=challenge_user.user_id,
        time_created=datetime.now(tz=timezone.utc),
    )
    db.add(new_challenge_user)
    db.commit()
    db.refresh(new_challenge_user)
    if not new_challenge_user:
        raise HTTPException(
            status_code=400, detail="User could not be added to challenge"
        )
    return new_challenge_user

def get_users_by_challenge_id(db: Session, challenge_id: int):
    challenge_users = db.query(ChallengeUser).filter(ChallengeUser.challenge_id == challenge_id).all()
    if not challenge_users:
        raise HTTPException(
            status_code=404, detail=f"No users found for challenge with ID {challenge_id}"
        )
    return challenge_users

def delete_user_from_challenge(db: Session, challenge_id: int, user_id: int):
    challenge_user = db.query(ChallengeUser).filter(ChallengeUser.challenge_id == challenge_id, ChallengeUser.user_id == user_id).first()
    if not challenge_user:
        raise HTTPException(
            status_code=404, detail=f"User not found for challenge with ID {challenge_id}"
        )
    db.delete(challenge_user)
    db.commit()
    return challenge_user

def get_challenges_by_user_id(db: Session, user_id: int):
    challenges = db.query(ChallengeUser).filter(ChallengeUser.user_id == user_id).all()
    if not challenges:
        raise HTTPException(
            status_code=404, detail=f"No challenges found for user with ID {user_id}"
        )
    return challenges

