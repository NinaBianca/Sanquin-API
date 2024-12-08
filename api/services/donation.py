from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..models.donation import Donation
from ..models.user import User

def check_donation_exists(db, donation_id):
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if not donation:
        return False
    return True

def create_donation(db: Session, donation: Donation):
    new_donation = Donation(
        amount=donation.amount,
        user_id=donation.user_id,
        time_created=datetime.now(tz=timezone.utc),
    )
    db.add(new_donation)
    db.commit()
    db.refresh(new_donation)
    if not new_donation:
        raise HTTPException(
            status_code=400, detail="Donation could not be created"
        )
    return new_donation

def get_donations_by_user_id(db: Session, user_id: int):
    donations = db.query(Donation).filter(Donation.user_id == user_id).all()
    if not donations:
        raise HTTPException(
            status_code=404, detail=f"No donations found for user with ID {user_id}"
        )
    return donations

def delete_donation(db: Session, donation_id: int):
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if not donation:
        raise HTTPException(
            status_code=404, detail=f"Donation not found with ID {donation_id}"
        )
    db.delete(donation)
    db.commit()
    return donation

def update_donation(db: Session, donation_id: int, donation_partial):
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if not donation:
        raise HTTPException(
            status_code=404, detail=f"Donation not found with ID {donation_id}"
        )
    donation_data = donation_partial.dict(exclude_unset=True)
    for key, value in donation_data.items():
        setattr(donation, key, value)
    db.add(donation)
    db.commit()
    db.refresh(donation)
    return donation

def get_donation_by_id(db: Session, donation_id: int):
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if not donation:
        raise HTTPException(
            status_code=404, detail=f"Donation not found with ID {donation_id}"
        )
    return donation
