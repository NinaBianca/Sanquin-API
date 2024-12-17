from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..models.donation import Donation
from ..models.user import User
from ..models.location_info import LocationInfo, Timeslot
from ..schemas.donation import LocationInfoCreate

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

def get_location_info_by_city(db: Session, city: str):
    location = db.query(LocationInfo).filter(LocationInfo.address.contains(city)).all()
    if not len(location) > 0:
        raise HTTPException(
            status_code=404, detail=f"Location not found in city {city}"
        )
    return location

def get_timeslots_by_location_id(db: Session, location_id: int):
    timeslots = db.query(Timeslot).filter(Timeslot.location_id == location_id).all()
    if not len(timeslots) > 0:
        raise HTTPException(
            status_code=404, detail=f"No timeslots found for location with ID {location_id}"
        )
    return timeslots

def create_location_info(db: Session, location_info: LocationInfoCreate):
    new_location = LocationInfo(
        name=location_info.name,
        address=location_info.address,
        opening_hours=location_info.opening_hours,
        latitude=location_info.latitude,
        longitude=location_info.longitude,
        timeslots=location_info.timeslots

    )
    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    if not new_location:
        raise HTTPException(
            status_code=400, detail="Location could not be created"
        )
    return new_location

def update_location_info(db: Session, location_id: int, location_info_partial):
    location = db.query(LocationInfo).filter(LocationInfo.id == location_id).first()
    if not location:
        raise HTTPException(
            status_code=404, detail=f"Location not found with ID {location_id}"
        )
    location_data = location_info_partial.dict(exclude_unset=True)
    for key, value in location_data.items():
        setattr(location, key, value)
    db.add(location)
    db.commit()
    db.refresh(location)
    return location

def delete_location_info(db: Session, location_id: int):
    location = db.query(LocationInfo).filter(LocationInfo.id == location_id).first()
    if not location:
        raise HTTPException(
            status_code=404, detail=f"Location not found with ID {location_id}"
        )
    db.delete(location)
    db.commit()
    return location