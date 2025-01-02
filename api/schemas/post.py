from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional 
from pydantic import Field, ConfigDict

class KudosBase(BaseModel):
    post_id: int = Field(...)
    user_id: int = Field(...)
    
    model_config = ConfigDict(from_attributes=True)

class KudosCreate(KudosBase):
    pass

class KudosResponse(KudosBase):
    id: int = Field(...)
    time_created: datetime = Field(...)

    def model_dump(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "user_id": self.user_id,
            "time_created": self.time_created
        }
        
class PostBase(BaseModel):
    title: str = Field(...)
    content: str = Field(...)
    post_type: str = Field(...)
    
    model_config = ConfigDict(from_attributes=True)

class PostCreate(PostBase):
    user_id: int = Field(...)

class PostResponse(PostBase):
    id: int = Field(...)
    user_id: int = Field(...)
    created_at: datetime = Field(...)
    kudos: List[KudosResponse] = Field(...)

    def model_dump(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at,
            "post_type": self.post_type,
            "kudos": [kudos.model_dump() for kudos in self.kudos]
        }  