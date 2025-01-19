from fastapi import HTTPException, APIRouter, Depends
from fastapi_cache.decorator import cache
import redis
import zlib
import os
import json
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.response import ResponseModel
from ..schemas.donation import DonationCreate, DonationBase, LocationInfoCreate, LocationInfoBase, LocationInfoResponse, Timeslot, DonationResponse, TimeslotResponse
from ..services.donation import (
    get_location_name_by_id,
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
    get_all_location_info,
    get_friends_donations
    
)
from ..services.user import check_user_exists

router = APIRouter(
    prefix="/donations",
    tags=["donations"],
)

@router.post("/", response_model=ResponseModel)
def create_new_donation(donation: DonationCreate, db: Session = Depends(get_db)):
    if not check_user_exists(db, donation.user_id):
        raise HTTPException(status_code=404, detail=f"User not found with ID {donation.user_id}")
    
    try:
        new_donation = create_donation(db=db, donation=donation)
        return ResponseModel(status=200, data=DonationResponse.model_validate(new_donation), message="Donation created successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the donation: {e}") from e

@router.get("/user/{user_id}", response_model=ResponseModel)
def read_donations_by_user_id(user_id: int, db: Session = Depends(get_db)):
    if not check_user_exists(db, user_id):
        raise HTTPException(status_code=404, detail=f"User not found with ID {user_id}")
    try:
        donations = get_donations_by_user_id(db=db, user_id=user_id)
        donations_list = [DonationResponse.model_validate(donation) for donation in donations]
        return ResponseModel(status=200, data=donations_list, message="Donations retrieved successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving donations: {e}") from e
    
@router.get("/user/{user_id}/friends", response_model=ResponseModel)
def read_friends_donations(user_id: int, db: Session = Depends(get_db)):
    if not check_user_exists(db, user_id):
        raise HTTPException(status_code=404, detail=f"User not found with ID {user_id}")
    try:
        friends_donations = get_friends_donations(db, user_id)
        friends_donations_list = [DonationResponse.model_validate(donation) for donation in friends_donations]
        return ResponseModel(status=200, data=friends_donations_list, message="Friends' donations retrieved successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving friends' donations: {e}") from e


@router.delete("/{donation_id}", response_model=ResponseModel)
def remove_donation(donation_id: int, db: Session = Depends(get_db)):
    try:
        delete_donation(db=db, donation_id=donation_id)
        return ResponseModel(status=200, message="Donation deleted successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while deleting the donation: {e}") from e

@router.put("/{donation_id}", response_model=ResponseModel)
def update_donation_route(donation_id: int, donation: DonationBase, db: Session = Depends(get_db)):
    try:
        updated_donation = update_donation(db, donation_id, donation)
        return ResponseModel(status=200, data=DonationResponse.model_validate(updated_donation), message="Donation updated successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the donation: {e}") from e

@router.get("/{donation_id}", response_model=ResponseModel)
def get_donation_route(donation_id: int, db: Session = Depends(get_db)):
    try:
        donation = get_donation_by_id(db, donation_id)
        donation_dict = DonationResponse.model_validate(donation)
        return ResponseModel(status=200, data=donation_dict, message="Donation retrieved successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving the donation: {e}") from e

@router.get("/location/all", response_model=ResponseModel)
@cache(600)
def get_all_location_info_route(db: Session = Depends(get_db)):
    try:
        cache_key = "locations_all"
        redis_client = redis.from_url(os.getenv("REDIS_URL"))
        compressed_data = redis_client.get(cache_key)

        if compressed_data:
            # Decompress the cached data
            decompressed_data = zlib.decompress(compressed_data).decode('utf-8')
            output = json.loads(decompressed_data)  # Convert back to Python object (list of locations)
            return ResponseModel(status=200, data=output, message="Location(s) retrieved successfully")
        
        # If not in cache, fetch from DB and compress it
        locations = get_all_location_info(db)
        output = [LocationInfoResponse.model_validate(location) for location in locations]

        # Convert to JSON and compress
        json_data = json.dumps(output)
        compressed_data = zlib.compress(json_data.encode('utf-8'))

        # Store the compressed data in Redis
        redis_client.setex(cache_key, 600, compressed_data)
        return ResponseModel(status=200, data=output, message="Location(s) retrieved successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving location information: {e}") from e

@router.get("/location/{city}", response_model=ResponseModel)
def get_location_info_by_city_route(city: str, db: Session = Depends(get_db)):
    try:
        locations = get_location_info_by_city(db, city)
        output = [LocationInfoResponse.model_validate(location) for location in locations]   
        return ResponseModel(status=200, data=output, message="Location(s) retrieved successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving location information: {e}") from e

@router.get("/location/{location_id}/name", response_model=ResponseModel)
def get_location_name_by_id_route(location_id: int, db: Session = Depends(get_db)):
    try:
        location = get_location_name_by_id(db, location_id)
        return ResponseModel(status=200, data={"name": location}, message="Location retrieved successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving location information: {e}") from e

@router.get("/location/{location_id}/timeslots", response_model=ResponseModel)
def get_timeslots_by_location_route(location_id: str, db: Session = Depends(get_db)):
    try:
        timeslots = get_timeslots_by_location_id(db, location_id)
        output = [TimeslotResponse.model_validate(timeslot) for timeslot in timeslots]
        
        return ResponseModel(status=200, data=output, message="Timeslots retrieved successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving timeslots: {e}") from e

@router.post("/location", response_model=ResponseModel)
def create_location_info_route(location: LocationInfoCreate, db: Session = Depends(get_db)):
    try:
        new_location = create_location_info(db, location)
        return ResponseModel(status=200, data=LocationInfoResponse.model_validate(new_location), message="Location created successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the location: {e}") from e

@router.put("/location/{location_id}", response_model=ResponseModel)
def update_location_info_route(location_id: int, location: LocationInfoBase, db: Session = Depends(get_db)):
    try:
        updated_location = update_location_info(db, location_id, location)
        return ResponseModel(status=200, data=LocationInfoResponse.model_validate(updated_location), message="Location updated successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the location information: {e}") from e

@router.delete("/location/{location_id}", response_model=ResponseModel)
def delete_location_info_route(location_id: int, db: Session = Depends(get_db)):
    try:
        delete_location_info(db, location_id)
        return ResponseModel(status=200, message="Location deleted successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while deleting the location information: {e}") from e