from typing import Optional
from pydantic import BaseModel, EmailStr


class UpdateUserModel(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
