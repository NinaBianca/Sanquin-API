from typing import List
from pydantic import BaseModel
from .user import UserModel


class UserCollection(BaseModel):
    users: List[UserModel]

    def model_dump(self):
        return [user.model_dump() for user in self.users]
    
    def __init__(self, **data):
        super().__init__(**data)
