from api.database import engine, Base
from api.models.user import User
from api.models.donation import Donation
from api.models.friend import Friend
from api.models.location_info import LocationInfo, Timeslot
from api.models.challenge import Challenge
from api.models.challenge_user import ChallengeUser
from api.models.post import Post
from api.models.kudos import Kudos

# Create all tables in the database
Base.metadata.create_all(bind=engine)

print("All tables created successfully.")