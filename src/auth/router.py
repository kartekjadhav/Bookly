from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from schemas.users import UserModel, UserCreateModel
from db.main import get_session
from .services import  UserServices


userRouter = APIRouter()
userServices = UserServices()

# Create User
@userRouter.post(
    path="/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=UserModel
)
async def create_user(userData: UserCreateModel, session:AsyncSession = Depends(get_session)):
    user_exists = await userServices.check_user_exits(email=userData.email, session=session)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User already exists with this email.")
    new_user = await userServices.create_user(userData=userData, session=session)
    return new_user