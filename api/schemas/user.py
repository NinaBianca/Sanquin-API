from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from models.enums import UserRole
from datetime import datetime, date

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    birthdate: datetime
    city: str
    current_points: Optional[int] = 200
    total_points: Optional[int] = 200
    role: Optional[UserRole] = UserRole.USER

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None)
    last_name: Optional[str] = Field(None)
    username: Optional[str] = Field(None)
    email: Optional[EmailStr] = Field(None)
    password: Optional[str] = Field(None)
    birthdate: Optional[datetime] = Field(None)
    city: Optional[str] = Field(None)
    current_points: Optional[int] = Field(None)
    total_points: Optional[int] = Field(None)
    role: Optional[UserRole] = Field(None)
    
    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    birthdate: datetime
    city: str
    current_points: int
    total_points: int
    role: UserRole
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)