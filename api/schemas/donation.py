from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional
from models.enums import DonationType, DonationStatus


class Timeslot(BaseModel):
    start_time: datetime = Field(...)
    end_time: datetime = Field(...)
    total_capacity: int = Field(...)
    remaining_capacity: int = Field(...)
    
    model_config = ConfigDict(from_attributes=True)
    
    def model_dump(self):
        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_capacity": self.total_capacity,
            "remaining_capacity": self.remaining_capacity
        }
    
    
        
class TimeslotResponse(Timeslot):
    id: int = Field(...)
    
    def model_dump(self):
        return {
            "id": self.id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_capacity": self.total_capacity,
            "remaining_capacity": self.remaining_capacity
        }

class LocationInfoBase(BaseModel):
    name: str = Field(...)
    address: str = Field(...)
    opening_hours: str = Field(...)
    latitude: str = Field(...)
    longitude: str = Field(...)
    timeslots: List[Timeslot] = Field(...)
    
    model_config = ConfigDict(from_attributes=True)

class LocationInfoCreate(LocationInfoBase):
    pass

class LocationInfoUpdate(LocationInfoBase):
    id: int = Field(...)
    pass

class LocationInfoResponse(LocationInfoBase):
    id: int = Field(...)
 
    def model_dump(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "opening_hours": self.opening_hours,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timeslots": self.timeslots
        }

class DonationBase(BaseModel):
    amount: Optional[float] = Field(...)
    user_id: int = Field(...)
    location_id: int = Field(...)
    donation_type: DonationType = Field(...)
    appointment: datetime = Field(...)
    status: DonationStatus = Field(...)
    enable_joining: bool = Field(...)
    
    model_config = ConfigDict(from_attributes=True)

class DonationCreate(DonationBase):
    pass

class DonationUpdate(DonationBase):
    id: int = Field(...)
    pass

class DonationResponse(DonationBase):
    id: int = Field(...)

    def model_dump(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "user_id": self.user_id,
            "location": self.location.model_dump(),
            "type": self.donation_type,
            "appointment": self.appointment,
            "status": self.status,
            "enable_joining": self.enable_joining
        }
    
