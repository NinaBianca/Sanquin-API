from typing import List
from pydantic import BaseModel
from .user import UserModel


class UserCollection(BaseModel):
    users: List[UserModel]
