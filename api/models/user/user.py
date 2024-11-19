from typing import Optional
from pydantic import BaseModel, Field, EmailStr, SecretStr
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from enum import Enum

PyObjectId = Annotated[str, BeforeValidator(str)]

class DonationType(str, Enum):
    BLOOD = "Blood"
    PLASMA = "Plasma"

class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: SecretStr = Field(...)
    can_donate: bool = Field(default=False) 
    donation_type: Optional[DonationType] = Field(...)

    def __init__(self, **data):
        super().__init__(**data)
    
    def model_dump(self):
        password = self.password.get_secret_value()
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "password": password,
            "can_donate": self.can_donate,
            "donation_type": self.donation_type
        }
