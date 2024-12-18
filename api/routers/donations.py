from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.response import ResponseModel
from ..schemas.donation import DonationCreate, DonationBase, LocationInfoCreate, LocationInfoBase, LocationInfoResponse
from ..services.donation import (
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
    get_timeslots_by_location_id
    
)
from ..services.user import check_user_exists

router = APIRouter(
    prefix="/donations",
    tags=["donations"],
)

@router.post("/", response_model=ResponseModel)
def create_new_donation(donation: DonationCreate, db: Session = Depends(get_db)):
    if not donation.amount or not donation.user_id:
        raise HTTPException(status_code=400, detail="Amount and user_id are required to create a donation")
    if not check_user_exists(db, donation.user_id):
        raise HTTPException(status_code=404, detail=f"User not found with ID {donation.user_id}")
    
    new_donation = create_donation(db=db, donation=donation)
    return ResponseModel(status=200, data=new_donation, message="Donation created successfully")

@router.get("/user/{user_id}", response_model=ResponseModel)
def read_donations_by_user_id(user_id: int, db: Session = Depends(get_db)):
    if not check_user_exists(db, user_id):
        raise HTTPException(status_code=404, detail=f"User not found with ID {user_id}")
    donations = get_donations_by_user_id(db=db, user_id=user_id)
    return ResponseModel(status=200, data=donations, message="Donations retrieved successfully")

@router.delete("/{donation_id}", response_model=ResponseModel)
def remove_donation(donation_id: int, db: Session = Depends(get_db)):
    if not check_donation_exists(db, donation_id):
        raise HTTPException(status_code=404, detail=f"Donation not found with ID {donation_id}")
    delete_donation(db=db, donation_id=donation_id)
    return ResponseModel(status=200, message="Donation deleted successfully")

@router.put("/{donation_id}", response_model=ResponseModel)
def update_donation_route(donation_id: int, donation: DonationBase, db: Session = Depends(get_db)):
    if not check_donation_exists(db, donation_id):
        raise HTTPException(status_code=404, detail=f"Donation not found with ID {donation_id}")
    updated_donation = update_donation(db, donation_id, donation)
    return ResponseModel(status=200, data=updated_donation, message="Donation updated successfully")

@router.get("/{donation_id}", response_model=ResponseModel)
def get_donation_route(donation_id: int, db: Session = Depends(get_db)):
    if not check_donation_exists(db, donation_id):
        raise HTTPException(status_code=404, detail=f"Donation not found with ID {donation_id}")
    donation = get_donation_by_id(db, donation_id)
    return ResponseModel(status=200, data=donation, message="Donation retrieved successfully")

@router.get("/location/{city}", response_model=ResponseModel)
def get_location_info_by_city_route(city: str, db: Session = Depends(get_db)):
    location = get_location_info_by_city(db, city)
    return ResponseModel(status=200, data=location, message="Location(s) retrieved successfully")

@router.get("/location/{city}/timeslots", response_model=ResponseModel)
def get_timeslots_by_location_route(city: str, db: Session = Depends(get_db)):
    timeslots = get_timeslots_by_location_id(db, city)
    return ResponseModel(status=200, data=timeslots, message="Timeslots retrieved successfully")

@router.post("/location", response_model=ResponseModel)
def create_location_info_route(location: LocationInfoCreate, db: Session = Depends(get_db)):
    new_location = create_location_info(db, location)
    return ResponseModel(status=200, data=LocationInfoResponse.from_attributes(new_location), message="Location created successfully")

@router.put("/location/{location_id}", response_model=ResponseModel)
def update_location_info_route(location_id: int, location: LocationInfoBase, db: Session = Depends(get_db)):
    updated_location = update_location_info(db, location_id, location)
    return ResponseModel(status=200, data=updated_location, message="Location updated successfully")

@router.delete("/location/{location_id}", response_model=ResponseModel)
def delete_location_info_route(location_id: int, db: Session = Depends(get_db)):
    delete_location_info(db, location_id)
    return ResponseModel(status=200, message="Location deleted successfully")