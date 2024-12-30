from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from models.enums import UserRole
from datetime import datetime, date

PyObjectId = Annotated[str, BeforeValidator(str)]


from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional
from models.enums import UserRole

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
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    birthdate: Optional[datetime]
    city: Optional[str]
    current_points: Optional[int]
    total_points: Optional[int]
    role: Optional[UserRole]
    
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