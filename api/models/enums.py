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

# class PostVisibility(str, Enum):
#     PUBLIC = "public"
#     FRIENDS_ONLY = "friends_only"
#     PRIVATE = "private"