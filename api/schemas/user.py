from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from models.enums import UserRole
from datetime import datetime, date

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserModel(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    birthdate: date = Field(...)
    city: str = Field(...)
    current_points: int = Field(default=200)
    total_points: int = Field(default=200)
    role: UserRole = Field(default=UserRole.USER)
    created_at: datetime = Field(default_factory=datetime.now)

    def __init__(self, **data):
        super().__init__(**data)
    
    def model_dump(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "birthdate": self.birthdate,
            "city": self.city,
            "current_points": self.current_points,  
            "total_points": self.total_points,
            "role": self.role,
            "created_at": self.created_at
        }

class UserCollection(BaseModel):
    users: List[UserModel]

    def model_dump(self):
        return [user.model_dump() for user in self.users]
    
    def __init__(self, **data):
        super().__init__(**data)

class UpdateUserModel(BaseModel):
    id: PyObjectId = Field(...)
    first_name: Optional[str] = Field(None)
    last_name: Optional[str] = Field(None)
    username: Optional[str] = Field(None)
    email: Optional[EmailStr] = Field(None)
    password: Optional[str] = Field(None)
    birthdate: Optional[date] = Field(None)
    city: Optional[str] = Field(None)
    current_points: Optional[int] = Field(None)
    total_points: Optional[int] = Field(None)

    def __init__(self, **data):
        super().__init__(**data)
    
    def model_dump(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "birthdate": self.birthdate,
            "city": self.city,
            "current_points": self.current_points,
            "total_points": self.total_points
        }
    