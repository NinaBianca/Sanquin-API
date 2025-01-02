from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class ChallengeBase(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
    location: str = Field(...)
    goal: float = Field(...)
    start: datetime = Field(...)
    end: datetime = Field(...)
    
    model_config = ConfigDict(from_attributes=True)

class ChallengeCreate(ChallengeBase):
    pass

class ChallengeUpdate(BaseModel):
    title: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    location: Optional[str] = Field(None)
    goal: Optional[float] = Field(None)
    start: Optional[datetime] = Field(None)
    end: Optional[datetime] = Field(None)
    

class ChallengeResponse(ChallengeBase):
    id: int = Field(...)

    def model_dump(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "goal": self.goal,
            "start": self.start,
            "end": self.end
        }
    

class ChallengeUserBase(BaseModel):
    challenge_id: int = Field(...)
    user_id: int = Field(...)
    status: str = Field(...)

class ChallengeUserCreate(ChallengeUserBase):
    pass

class ChallengeUserResponse(ChallengeUserBase):

    def model_dump(self):
        return {
            "challenge_id": self.challenge_id,
            "user_id": self.user_id,
            "status": self.status
        }