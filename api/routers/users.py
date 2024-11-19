from fastapi import APIRouter, params
from dependencies import get_db
from models.user.user_collection import UserCollection
from models.user.user import UserModel
from models.user.update_user import UpdateUserModel
from models.response import ResponseModel
from fastapi import HTTPException

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

user_collection = get_db().get_collection("users")


@router.get("/", tags=["users"]) # TODO: Double check if applicable to use case
async def read_users(skip: int = 0, limit: int = 20):
    try:
        users = await user_collection.find().skip(skip).limit(limit).to_list(limit)
        return ResponseModel(
            status=200,
            data=UserCollection(users=users).model_dump(),
            message="Users retrieved successfully",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {e}"
        )


@router.post("/", response_model=ResponseModel, tags=["users"])
async def create_user(user: UserModel):
    if user is None:
        raise HTTPException(
            status_code=500,
            detail="User data is required",
        )
    try:
        existing_user = await user_collection.find_one(
            {"$or": [{"username": user.username}, {"email": user.email}]}
        )
        if existing_user:
            if existing_user["username"] == user.username:
                raise HTTPException(
                    status_code=500,
                    detail="Username already exists",
                )
            if existing_user["email"] == user.email:
                raise HTTPException(
                    status_code=500,
                    detail="Email already exists",
                )
        
        user = await user_collection.insert_one(user.model_dump())
        return ResponseModel(
            status=200,
            data=UserModel(**user).model_dump(),
            message="User created successfully",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {e}"
        )


@router.post("/login", response_model=ResponseModel, tags=["users"])
async def login_user(user: UserModel):
    if user is None:
        raise HTTPException(
            status_code=500,
            detail="User data is required",
        )
    try:
        existing_user = await user_collection.find_one(
            {"$and": [{"username": user.username}, {"password": user.password}]}
        )
        if existing_user:
            return ResponseModel(
                status=200,
                data=UserModel(**existing_user).model_dump(),
                message="User logged in successfully",
            )
        raise HTTPException(
            status_code=500,
            detail="Invalid username or password",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {e}"
        )


@router.put("/{user_id}", response_model=ResponseModel, tags=["users"])
async def update_user(user_id: int, user: UpdateUserModel):
    if user is None:
        raise HTTPException(
            status_code=500,
            detail="User data is required",
        )
    
    try:
        existing_user = await user_collection.find_one({"_id": user_id})
        if existing_user:
            user = await user_collection.update_one(
                {"_id": user_id}, {"$set": user.model_dump()}
            )
            return ResponseModel(
                status=200,
                data=UserModel(**user).model_dump(),
                message="User updated successfully",
            )
        raise HTTPException(
            status_code=500,
            detail="User not found",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {e}"
        )
