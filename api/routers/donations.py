from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.response import ResponseModel
from schemas.donation import DonationCreate, DonationBase, LocationInfoCreate, LocationInfoBase, LocationInfoResponse, Timeslot, DonationResponse, TimeslotResponse
from services.donation import (
    check_donation_exists,
    create_donation,
    get_donations_by_user_id,
    delete_donation,
    update_donation,
    get_donation_by_id,
    create_location_info,
    update_location_info,
    delete_location_info,
    get_location_info_by_city,
    get_timeslots_by_location_id,
    get_all_location_info
    
)
from services.user import check_user_exists

import logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/donations",
    tags=["donations"],
)

@router.post("/", response_model=ResponseModel)
def create_new_donation(donation: DonationCreate, db: Session = Depends(get_db)):
    logger.info(f"Received request to create donation for user ID: {donation.user_id} with amount: {donation.amount}")
    if not check_user_exists(db, donation.user_id):
        logger.warning(f"User not found with ID: {donation.user_id}")
        raise HTTPException(status_code=404, detail=f"User not found with ID {donation.user_id}")
    
    try:
        new_donation = create_donation(db=db, donation=donation)
        logger.info(f"Donation created successfully for user ID: {donation.user_id}")
        return ResponseModel(status=200, data=DonationResponse.model_validate(new_donation), message="Donation created successfully")
    except Exception as e:
        logger.error(f"Error creating donation: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the donation.") from e

@router.get("/user/{user_id}", response_model=ResponseModel)
def read_donations_by_user_id(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Received request to retrieve donations for user ID: {user_id}")
    if not check_user_exists(db, user_id):
        logger.warning(f"User not found with ID: {user_id}")
        raise HTTPException(status_code=404, detail=f"User not found with ID {user_id}")
    try:
        donations = get_donations_by_user_id(db=db, user_id=user_id)
        logger.info(f"Donations retrieved successfully for user ID: {user_id}")
        donations_list = [DonationResponse.model_validate(donation) for donation in donations]
        return ResponseModel(status=200, data=donations_list, message="Donations retrieved successfully")
    except HTTPException as e:
        logger.error(f"An error occurred while retrieving donations: {e}")
        raise e
    except Exception as e:
        logger.error(f"An error occurred while retrieving donations: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving donations.") from e


@router.delete("/{donation_id}", response_model=ResponseModel)
def remove_donation(donation_id: int, db: Session = Depends(get_db)):
    try:
        delete_donation(db=db, donation_id=donation_id)
        return ResponseModel(status=200, message="Donation deleted successfully")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while deleting the donation.") from e

@router.put("/{donation_id}", response_model=ResponseModel)
def update_donation_route(donation_id: int, donation: DonationBase, db: Session = Depends(get_db)):
    try:
        updated_donation = update_donation(db, donation_id, donation)
        return ResponseModel(status=200, data=updated_donation, message="Donation updated successfully")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while updating the donation.") from e

@router.get("/{donation_id}", response_model=ResponseModel)
def get_donation_route(donation_id: int, db: Session = Depends(get_db)):
    try:
        donation = get_donation_by_id(db, donation_id)
        donation_dict = DonationResponse.model_validate(donation)
        return ResponseModel(status=200, data=donation_dict, message="Donation retrieved successfully")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the donation.") from e

@router.get("/location/all", response_model=ResponseModel)
def get_all_location_info_route(db: Session = Depends(get_db)):
    try:
        logger.info("Received request to retrieve all location information")
        locations = get_all_location_info(db)
        output = [LocationInfoResponse.model_validate(location) for location in locations]
        return ResponseModel(status=200, data=output, message="Location(s) retrieved successfully")
    except HTTPException as e:
        logger.error(f"An error occurred while retrieving location information: {e}")
        raise e
    except Exception as e:
        logger.error(f"An error occurred while retrieving location information: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving location information.") from e

@router.get("/location/{city}", response_model=ResponseModel)
def get_location_info_by_city_route(city: str, db: Session = Depends(get_db)):
    try:
        logger.info(f"Received request to retrieve location information for city: {city}")
        locations = get_location_info_by_city(db, city)
        output = [LocationInfoResponse.model_validate(location) for location in locations]   
        return ResponseModel(status=200, data=output, message="Location(s) retrieved successfully")
    except HTTPException as e:
        logger.error(f"An error occurred while retrieving location information: {e}")
        raise e
    except Exception as e:
        logger.error(f"An error occurred while retrieving location information: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving location information.") from e

@router.get("/location/{location_id}/timeslots", response_model=ResponseModel)
def get_timeslots_by_location_route(location_id: str, db: Session = Depends(get_db)):
    try:
        timeslots = get_timeslots_by_location_id(db, location_id)
        output = [TimeslotResponse.model_validate(timeslot) for timeslot in timeslots]
        
        return ResponseModel(status=200, data=output, message="Timeslots retrieved successfully")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving timeslots.") from e

@router.post("/location", response_model=ResponseModel)
def create_location_info_route(location: LocationInfoCreate, db: Session = Depends(get_db)):
    try:
        new_location = create_location_info(db, location)
        return ResponseModel(status=200, data=LocationInfoResponse.model_validate(new_location), message="Location created successfully")
    except Exception as e:
        logger.error(f"Error creating location info: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the location.") from e

@router.put("/location/{location_id}", response_model=ResponseModel)
def update_location_info_route(location_id: int, location: LocationInfoBase, db: Session = Depends(get_db)):
    logger.info(f"Received request to update location info with ID: {location_id}")
    try:
        updated_location = update_location_info(db, location_id, location)
        logger.info(f"Location info updated successfully with ID: {location_id}")
        return ResponseModel(status=200, data=LocationInfoResponse.model_validate(updated_location), message="Location updated successfully")
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error updating location info: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the location information.") from e

@router.delete("/location/{location_id}", response_model=ResponseModel)
def delete_location_info_route(location_id: int, db: Session = Depends(get_db)):
    logger.info(f"Received request to delete location info with ID: {location_id}")
    try:
        delete_location_info(db, location_id)
        logger.info(f"Location info deleted successfully with ID: {location_id}")
        return ResponseModel(status=200, message="Location deleted successfully")
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error deleting location info: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while deleting the location information.") from e