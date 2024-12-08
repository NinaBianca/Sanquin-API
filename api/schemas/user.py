from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from ..models.enums import UserRole
from datetime import datetime, date

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    birthdate: date = Field(...)
    city: str = Field(...)
    points: int = Field(default=0)
    role: UserRole = Field(default=UserRole.USER)
    created_at: datetime = Field(default_factory=datetime.now)

    def __init__(self, **data):
        super().__init__(**data)
    
    def model_dump(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "birthdate": self.birthdate,
            "city": self.city,
            "points": self.points,
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
    username: Optional[str] = Field(None)
    email: Optional[EmailStr] = Field(None)
    password: Optional[str] = Field(None)
    birthdate: Optional[date] = Field(None)
    city: Optional[str] = Field(None)
    points: Optional[int] = Field(None)
    created_at: Optional[datetime] = Field(None)

    def __init__(self, **data):
        super().__init__(**data)
    
    def model_dump(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "birthdate": self.birthdate,
            "city": self.city,
            "points": self.points,
            "role": self.role,
            "created_at": self.created_at
        }
    