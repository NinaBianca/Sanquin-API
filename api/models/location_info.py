from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Config:
    arbitrary_types_allowed = True

class LocationInfo(Base):
    __tablename__ = "location_info"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    address = Column(Text, nullable=False)
    opening_hours = Column(Text, nullable=False)
    latitude = Column(Text, nullable=False)
    longitude = Column(Text, nullable=False)

    timeslots = relationship("Timeslot", backref="location")

    def __repr__(self):
        return f"<LocationInfo(id={self.id}, name={self.name}, address={self.address}, city={self.city}, opening_hours={self.opening_hours}, latitude={self.latitude}, longitude={self.longitude})>"
    
class Timeslot(Base):
    __tablename__ = "timeslots"

    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("location_info.id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    total_capacity = Column(Integer, nullable=False)
    remaining_capacity = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Timeslot(id={self.id}, location_id={self.location_id}, start_time={self.start_time}, end_time={self.end_time}, capacity={self.capacity})>"