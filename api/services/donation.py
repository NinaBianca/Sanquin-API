from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc

from models.donation import Donation
from models.user import User
from models.location_info import LocationInfo, Timeslot
from schemas.donation import LocationInfoCreate, DonationCreate

import logging
logger = logging.getLogger(__name__)

def check_donation_exists(db, donation_id):
    logger.info(f"Checking if donation exists with ID: {donation_id}")
    return db.query(Donation).filter(Donation.id == donation_id).first() is not None
    
def check_location_exists(db, location_id):
    logger.info(f"Checking if location exists with ID: {location_id}")
    return db.query(LocationInfo).filter(LocationInfo.id == location_id).first() is not None
    
def create_donation(db: Session, donation: DonationCreate):
    logger.info(f"Creating donation with amount: {donation.amount} for user ID: {donation.user_id}")
    try: 
        new_donation = Donation(
            user_id=donation.user_id,
            location_id=donation.location_id,
            type=donation.donation_type,
            amount=donation.amount,
            appointment=donation.appointment,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        db.add(new_donation)
        db.commit()
        db.refresh(new_donation)
        return new_donation
    except SQLAlchemyError as e:
        logger.error(f"Error creating donation: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")

def get_donations_by_user_id(db: Session, user_id: int):
    logger.info(f"Retrieving donations for user with ID: {user_id}")
    try:
        donations = db.query(Donation).filter(Donation.user_id == user_id).all()
        if not donations:
            raise HTTPException(
                status_code=404, detail=f"No donations found for user with ID {user_id}"
            )
        return donations
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the donations.") from e

def delete_donation(db: Session, donation_id: int):
    logger.info(f"Deleting donation with ID: {donation_id}")
    try:
        if not check_donation_exists(db, donation_id):
            raise HTTPException(
                status_code=404, detail=f"Donation not found with ID {donation_id}"
            )
        donation = db.query(Donation).filter(Donation.id == donation_id).first()
        if not donation:
            raise HTTPException(
                status_code=404, detail=f"Donation not found with ID {donation_id}"
            )
        db.delete(donation)
        db.commit()
        return donation
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while deleting the donation.") from e

def update_donation(db: Session, donation_id: int, donation_partial):
    logger.info(f"Updating donation with ID: {donation_id}")
    try:
        if not check_donation_exists(db, donation_id):
            raise HTTPException(
                status_code=404, detail=f"Donation not found with ID {donation_id}"
            )
        donation = db.query(Donation).filter(Donation.id == donation_id).first()
        if not donation:
            raise HTTPException(
                status_code=404, detail=f"Donation not found with ID {donation_id}"
            )
        donation_data = donation_partial.dict(exclude_unset=True)
        for key, value in donation_data.items():
            setattr(donation, key, value)
        donation.updated_at = datetime.now(timezone.utc)
        db.add(donation)
        db.commit()
        db.refresh(donation)
        return donation
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while updating the donation.") from e

def get_donation_by_id(db: Session, donation_id: int):
    logger.info(f"Retrieving donation with ID: {donation_id}")
    try:
        if not check_donation_exists(db, donation_id):
            raise HTTPException(
                status_code=404, detail=f"Donation not found with ID {donation_id}"
            )
        donation = db.query(Donation).filter(Donation.id == donation_id).first()
        if not donation:
            raise HTTPException(
                status_code=404, detail=f"Donation not found with ID {donation_id}"
            )
        return donation
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the donation.") from e

def get_all_location_info(db: Session):
    try:
        locations = db.query(LocationInfo).all()
        logger.info("Locations retrieved: {locations}")
        if not locations:
            raise HTTPException(
                status_code=404, detail=f"No locations found"
            )
        return locations
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the locations.") from e

def get_location_info_by_city(db: Session, city: str):
    try:
        locations = db.query(LocationInfo).filter(LocationInfo.address.contains(city)).all()
        if not locations:
            raise HTTPException(
                status_code=404, detail=f"Location not found in city {city}"
            )
        return locations
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the locations.") from e

def get_timeslots_by_location_id(db: Session, location_id: int):
    try:
        timeslots = db.query(Timeslot).filter(Timeslot.location_id == location_id).all()
        if not timeslots:
            raise HTTPException(
                status_code=404, detail=f"No timeslots found for location with ID {location_id}"
            )
        return timeslots
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the timeslots.") from e

def create_location_info(db: Session, location_info: LocationInfoCreate):
    try:
        new_location = LocationInfo(
            name=location_info.name,
            address=location_info.address,
            opening_hours=location_info.opening_hours,
            latitude=location_info.latitude,
            longitude=location_info.longitude,
            timeslots=location_info.timeslots,
        )
        db.add(new_location)
        db.commit()
        db.refresh(new_location)
        if not new_location:
            raise HTTPException(
                status_code=400, detail="Location could not be created"
            )
        return new_location
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while creating the location.") from e

def update_location_info(db: Session, location_id: int, location_info_partial):
    try:
        if not check_location_exists(db, location_id):
            raise HTTPException(
                status_code=404, detail=f"Location not found with ID {location_id}"
            )
        location = db.query(LocationInfo).filter(LocationInfo.id == location_id).first()
        location_data = location_info_partial.dict(exclude_unset=True)
        for key, value in location_data.items():
            setattr(location, key, value)
        db.add(location)
        db.commit()
        db.refresh(location)
        return location
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while updating the location.") from e

def delete_location_info(db: Session, location_id: int):
    try:
        if not check_location_exists(db, location_id):
            raise HTTPException(
                status_code=404, detail=f"Location not found with ID {location_id}"
            )
        location = db.query(LocationInfo).filter(LocationInfo.id == location_id).first()
        db.delete(location)
        db.commit()
        return location
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while deleting the location.") from e