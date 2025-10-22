from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import timedelta, datetime

from schemas.users import UserModel, UserCreateModel, UserLoginModel
from db.main import get_session
from .services import UserServices
from .utils import decode_token, create_access_token, verify_password
from .dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
from db.redis import add_jti_to_blocklist, check_jti_in_blocklist

REFRESH_TOKEN_EXPIRY = 2

userRouter = APIRouter()
userServices = UserServices()
roleChecker = RoleChecker(['admin', 'user'])

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
                    'uid': str(user.uid),
                    'role': user.role
                }
            )

            refreshToken = create_access_token(
                userData={
                    'email': user.email,
                    'uid': str(user.uid),
                    'role': user.role
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

@userRouter.get("/refresh_token")
async def get_new_access_token(userData:dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = userData['exp']
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
            userData=userData['user']
        )
        return JSONResponse(
            content={'access_token':new_access_token}
        )
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Refresh token has expired.")

@userRouter.get("/me", response_model=UserModel)
async def get_current_user_details(user = Depends(get_current_user), _:bool=Depends(roleChecker)):
    return user

@userRouter.get("/logout")
async def revoke_token(userData:dict=Depends(AccessTokenBearer())):
    jti = userData['jti']
    await add_jti_to_blocklist(jti)
    return JSONResponse(content={
            "message": "Logged out successfully."
        },
        status_code=status.HTTP_200_OK
    )   
