from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..models.challenge import Challenge
from ..models.challenge_user import ChallengeUser
from ..models.enums import FriendshipStatus
from ..models.friend import Friend
from ..models.donation import Donation
from ..schemas.challenge import ChallengeCreate, ChallengeUpdate


def check_challenge_exists(db: Session, challenge_id: int) -> bool:
    result = db.execute(select(Challenge).filter(Challenge.id == challenge_id))
    return result.scalars().first() is not None

def create_challenge(db: Session, challenge: ChallengeCreate) -> Challenge:
    try:
        new_challenge = Challenge(
            title=challenge.title,
            description=challenge.description,
            location=challenge.location,
            goal=challenge.goal,
            start=challenge.start,
            end=challenge.end,
            reward_points=challenge.reward_points,
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
        raise HTTPException(status_code=500, detail=str(e)) from e

def get_challenges(db: Session):
    try:
        result = db.execute(select(Challenge))
        challenges = result.scalars().all()
        if not challenges:
            raise HTTPException(
                status_code=404, detail="No challenges found"
            )
        
        # Calculate total contributions for each challenge
        for challenge in challenges:
            total_contributions = calculate_total_contributions(db, challenge.id, challenge.start, challenge.end)
            challenge.total_contributions = total_contributions
        
        return challenges
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

def get_challenge_by_id(db: Session, challenge_id: int):
    try:
        if not check_challenge_exists(db, challenge_id):
            raise HTTPException(
                status_code=404, detail=f"Challenge not found with ID {challenge_id}"
            )
        result = db.execute(select(Challenge).filter(Challenge.id == challenge_id))
        challenge = result.scalars().first()
        if not challenge:
            raise HTTPException(
                status_code=404, detail=f"Challenge not found with ID {challenge_id}"
            )
        
        # Calculate total contributions for the challenge
        total_contributions = calculate_total_contributions(db, challenge.id, challenge.start, challenge.end)
        challenge.total_contributions = total_contributions
        print(challenge.total_contributions)
        return challenge
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

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
        raise HTTPException(status_code=500, detail=str(e)) from e

def delete_challenge(db: Session, challenge_id: int):
    try:
        if not check_challenge_exists(db, challenge_id):
            raise HTTPException(
                status_code=404, detail=f"Challenge not found with ID {challenge_id}"
            )
        result = db.execute(select(Challenge).filter(Challenge.id == challenge_id))
        challenge = result.scalars().first()
        if not challenge:
            raise HTTPException(
                status_code=404, detail=f"Challenge not found with ID {challenge_id}"
            )
        db.delete(challenge)
        db.commit()
        return challenge
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e)) from e

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
        raise HTTPException(status_code=500, detail=str(e)) from e

def get_users_by_challenge_id(db: Session, challenge_id: int):
    try:
        if not check_challenge_exists(db, challenge_id):
            raise HTTPException(
                status_code=404, detail=f"Challenge not found with ID {challenge_id}"
            )
        result = db.execute(select(ChallengeUser).filter(ChallengeUser.challenge_id == challenge_id))
        challenge_users = result.scalars().all()
        if not challenge_users:
            raise HTTPException(
                status_code=404, detail=f"No users found for challenge with ID {challenge_id}"
            )
        users = [challenge_user.user for challenge_user in challenge_users]
        for user in users:
            user.total_contributions = calculate_total_contributions(db, challenge_id, user.start, user.end)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

def delete_user_from_challenge(db: Session, challenge_id: int, user_id: int):
    try:
        if not check_challenge_exists(db, challenge_id):
            raise HTTPException(
                status_code=404, detail=f"Challenge not found with ID {challenge_id}"
            )
        result = db.execute(select(ChallengeUser).filter(ChallengeUser.challenge_id == challenge_id, ChallengeUser.user_id == user_id))
        challenge_user = result.scalars().first()
        if not challenge_user:
            raise HTTPException(
                status_code=404, detail=f"User not found for challenge with ID {challenge_id}"
            )
        db.delete(challenge_user)
        db.commit()
        return challenge_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e)) from e

def get_challenges_by_user_id(db: Session, user_id: int):
    try:
        result = db.execute(select(ChallengeUser).filter(ChallengeUser.user_id == user_id))
        challenges = result.scalars().all()
        if not challenges:
            raise HTTPException(
                status_code=404, detail=f"No challenges found for user with ID {user_id}"
            )
        
        # Calculate total contributions for each challenge
        for challenge_user in challenges:
            challenge = challenge_user.challenge
            total_contributions = calculate_total_contributions(db, challenge.id, challenge.start, challenge.end)
            challenge.total_contributions = total_contributions
        
        return [challenge_user.challenge for challenge_user in challenges]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    
def get_friends_by_challenge_id(db: Session, challenge_id: int, user_id: int):
    try:
        if not check_challenge_exists(db, challenge_id):
            raise HTTPException(
                status_code=404, detail=f"Challenge not found with ID {challenge_id}"
            )
        # Get the list of users participating in the challenge
        result = db.execute(select(ChallengeUser).filter(ChallengeUser.challenge_id == challenge_id))
        challenge_users = result.scalars().all()
        if not challenge_users:
            raise HTTPException(
                status_code=404, detail=f"No users found for challenge with ID {challenge_id}"
            )
        
        # Get the list of friends for the specified user
        friends = db.query(Friend).filter(
            or_(Friend.sender_id == user_id, Friend.receiver_id == user_id),
            Friend.status == FriendshipStatus.ACCEPTED
        ).all()
        
        friend_ids = {friend.sender_id if friend.sender_id != user_id else friend.receiver_id for friend in friends}
        
        # Filter the list of challenge participants to include only those who are friends with the specified user
        friends_participating = [challenge_user.user for challenge_user in challenge_users if challenge_user.user_id in friend_ids]
        for friend in friends_participating:
            friend.total_contributions = calculate_total_contributions(db, challenge_id, friend.start, friend.end)
        return friends_participating
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

def calculate_total_contributions(db: Session, challenge_id: int, start: datetime, end: datetime) -> float:
    result = db.execute(
        select(func.sum(Donation.amount))
        .join(ChallengeUser, Donation.user_id == ChallengeUser.user_id)
        .filter(
            ChallengeUser.challenge_id == challenge_id,
            Donation.appointment >= start,
            Donation.appointment <= end
        )
    )
    total_contributions = result.scalar()
    return total_contributions or 0.0
    