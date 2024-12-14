from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.response import ResponseModel
from schemas.donation import DonationCreate, DonationBase
from services.donation import (
    check_donation_exists,
    create_donation,
    get_donations_by_user_id,
    delete_donation,
    update_donation,
    get_donation_by_id
)
from services.user import check_user_exists

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


