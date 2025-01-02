from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from ..models.enums import FriendshipStatus
from datetime import datetime, date

PyObjectId = Annotated[str, BeforeValidator(str)]


class FriendRequestModel(BaseModel):
    sender_id: PyObjectId = Field(...)
    receiver_id: PyObjectId = Field(...)
    created_at: datetime = Field(default=datetime.now)
    status: FriendshipStatus = Field(default=FriendshipStatus.PENDING)
    
    model_config = ConfigDict(from_attributes=True)

    def __init__(self, **data):
        super().__init__(**data)
    
    def model_dump(self):
        return {
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "created_at": self.created_at,
            "status": self.status
        }

class FriendRequestCollection(BaseModel):
    requests: List[FriendRequestModel]

    def model_dump(self):
        return [request.model_dump() for request in self.requests]
    
    def __init__(self, **data):
        super().__init__(**data)

class UpdateFriendRequestModel(BaseModel):
    status: Optional[FriendshipStatus] = Field(None)

    def __init__(self, **data):
        super().__init__(**data)
    
    def model_dump(self):
        return {
            "status": self.status
        }
    