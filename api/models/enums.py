from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class FriendshipStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    BLOCKED = "blocked"

class DonationType(str, Enum):
    BLOOD = "blood"
    PLASMA = "plasma"

class DonationStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    CANCELLED = "cancelled"