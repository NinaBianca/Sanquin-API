from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class PostBase(BaseModel):
    content: str

class PostCreate(PostBase):
    user_id: int

class PostResponse(PostBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    def model_dump(self):
        return {
            "id": self.id,
            "content": self.content,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }   

class KudosBase(BaseModel):
    post_id: int
    user_id: int

class KudosCreate(KudosBase):
    pass

class KudosResponse(KudosBase):
    id: int
    time_created: datetime

    def model_dump(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "user_id": self.user_id,
            "time_created": self.time_created
        }