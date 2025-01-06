from pydantic.main import BaseModel, ConfigDict
from pydantic import Field
from datetime import datetime

class NotificationBase(BaseModel):
    title: str = Field(...)
    content: str = Field(...)
    user_id: int = Field(...)

class NotificationCreate(NotificationBase):
    pass

class NotificationResponse(NotificationBase):
    id: int = Field(...)
    created_at: datetime = Field(...)
    retrieved: bool = Field(...)

    model_config = ConfigDict(from_attributes=True)