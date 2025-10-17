from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import timedelta

from schemas.users import UserModel, UserCreateModel, UserLoginModel
from db.main import get_session
from .services import UserServices
from .utils import verify_access_token, create_access_token, verify_password

REFRESH_TOKEN_EXPIRY = 2

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

@userRouter.post(path="/login")
async def login_users(userData:UserLoginModel, session:AsyncSession=Depends(get_session)):
    email = userData.email
    password = userData.password

    user = await userServices.get_user_by_email(email=email, session=session)

    if user is not None:
        verify = verify_password(password=password, hash=user.password_hash)

        if verify:
            accessToken = create_access_token(
                userData={
                    'email': user.email,
                    'uid': str(user.uid)
                }
            )

            refreshToken = create_access_token(
                userData={
                    'email': user.email,
                    'uid': str(user.uid)
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )

            return JSONResponse(
                content={
                    "message": "You have successfully logged in.",
                    "accessToken": accessToken,
                    "refreshToken": refreshToken,
                    "userData": {
                        'email': email,
                        'uid': str(user.uid)
                    }
                },
                status_code=status.HTTP_200_OK
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} not found"
        )
