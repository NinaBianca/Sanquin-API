from fastapi import APIRouter
from dependencies import get_db
from models.user.user_collection import UserCollection
from models.user.user import UserModel

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

user_collection = get_db().get_collection("users")


@router.get("/", tags=["users"])
async def read_users():
    users = await user_collection.find().to_list(1000)
    return UserCollection(users=users)


@router.get("/{user_id}", tags=["users"])
async def read_user(user_id: int):
    return {"username": "fakeuser", "user_id": user_id}


@router.post("/", tags=["users"])
async def create_user(user: UserModel):
    # await user_collection.insert_one(user)
    return {"user": user, "status": "created"}


@router.put("/{user_id}", tags=["users"])
async def update_user(user_id: int):
    return {"user_id": user_id, "status": "updated"}
