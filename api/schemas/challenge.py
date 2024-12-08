from pydantic import BaseModel, Field
from datetime import datetime

class ChallengeBase(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
    location: str = Field(...)
    goal: float = Field(...)
    start: datetime = Field(...)
    end: datetime = Field(...)

class ChallengeCreate(ChallengeBase):
    pass

class ChallengeResponse(ChallengeBase):
    id: int = Field(...)
    total: float = Field(...)

    def model_dump(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "goal": self.goal,
            "start": self.start,
            "end": self.end,
            "total": self.total 
        }
    

class ChallengeUserBase(BaseModel):
    challenge_id: int = Field(...)
    user_id: int = Field(...)
    status: str = Field(...)
    progress: float = Field(...)

class ChallengeUserCreate(ChallengeUserBase):
    pass

class ChallengeUserResponse(ChallengeUserBase):
    id: int = Field(...)

    def model_dump(self):
        return {
            "id": self.id,
            "challenge_id": self.challenge_id,
            "user_id": self.user_id,
            "status": self.status,
            "progress": self.progress
        }