from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class LocationInfo(Base):
    __tablename__ = "location_info"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    address = Column(Text, nullable=False)
    opening_hours = Column(Text, nullable=False)
    latitude = Column(Text, nullable=False)
    longitude = Column(Text, nullable=False)

    timeslots = relationship("Timeslot", back_populates="location", cascade="all, delete-orphan")
    donations = relationship("Donation", back_populates="location")

    def __repr__(self):
        return f"<LocationInfo(id={self.id}, name={self.name}, address={self.address}, opening_hours={self.opening_hours}, latitude={self.latitude}, longitude={self.longitude})>"

class Timeslot(Base):
    __tablename__ = "timeslots"

    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("location_info.id", ondelete="CASCADE"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    total_capacity = Column(Integer, nullable=False)
    remaining_capacity = Column(Integer, nullable=False)

    location = relationship("LocationInfo", back_populates="timeslots")

    def __repr__(self):
        return f"<Timeslot(id={self.id}, location_id={self.location_id}, start_time={self.start_time}, end_time={self.end_time}, total_capacity={self.total_capacity}, remaining_capacity={self.remaining_capacity})>"