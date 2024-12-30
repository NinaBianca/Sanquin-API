from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from .enums import UserRole
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    birthdate = Column(DateTime, nullable=False)
    city = Column(String, nullable=False)
    blood_type = Column(String, nullable=True)
    nationality = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    is_eligible = Column(Boolean, nullable=True, default=False)
    current_points = Column(Integer, default=200)
    total_points = Column(Integer, default=200)
    role = Column(Enum(UserRole), default=UserRole.USER)
    created_at = Column(DateTime, default=datetime.now)

    # Relationship to donations
    donations = relationship("Donation", back_populates="user", cascade="all, delete-orphan")

    # Relationship to challenges (all challenges linked to user)
    challenges = relationship("ChallengeUser", back_populates="user", cascade="all, delete-orphan")

    # Relationships for friends
    sent_requests = relationship("Friend", foreign_keys="[Friend.sender_id]", back_populates="sender", cascade="all, delete-orphan")
    received_requests = relationship("Friend", foreign_keys="[Friend.receiver_id]", back_populates="receiver", cascade="all, delete-orphan")

    # Relationships for posts and kudos
    created_posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    liked_posts = relationship("Kudos", back_populates="user", cascade="all, delete-orphan")

    def model_dump(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "birthdate": self.birthdate,
            "city": self.city,
            "current_points": self.current_points,
            "total_points": self.total_points,
            "role": self.role,
            "created_at": self.created_at
        }
        