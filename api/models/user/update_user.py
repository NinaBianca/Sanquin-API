from typing import Optional
from pydantic import BaseModel, EmailStr, SecretStr


class UpdateUserModel(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[SecretStr] = None
    can_donate: Optional[bool] = None
    donation_type: Optional[str] = None

    
    def __init__(self, **data):
        super().__init__(**data)

    
    def model_dump(self):
        self.password = self.password.get_secret_value()
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "can_donate": self.can_donate,
            "donation_type": self.donation_type
        }
    
  
