from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Kudos(Base):
    __tablename__ = "kudos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    # Relationship to Post
    post = relationship("Post", back_populates="kudos_list")
    user = relationship("User", back_populates="liked_posts")

    def __repr__(self):
        return f"<Kudos(id={self.id}, user_id={self.user_id}, post_id={self.post_id}, created_at={self.created_at})>"