from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class DonationBase(BaseModel):
    amount: float = Field(...)
    user_id: int = Field(...)
    location: str = Field(...)
    type: str = Field(...)
    appointment: datetime = Field(...)
    status: str = Field(...)

class DonationCreate(DonationBase):
    pass

class DonationResponse(DonationBase):
    id: int = Field(...)

    def model_dump(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "user_id": self.user_id,
            "location": self.location,
            "type": self.type,
            "appointment": self.appointment,
            "status": self.status
        }