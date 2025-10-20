from fastapi import Request, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.auth.utils import decode_token
from db.redis import check_jti_in_blocklist
from typing import List
from src.auth.services import UserServices
from sqlmodel.ext.asyncio.session import AsyncSession
from db.main import get_session
from models.models import User

userServices = UserServices() 

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request:Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request=request)

        token = creds.credentials
        token_data = self.token_valid(token)
        if token_data is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid or expired token.")

        if await check_jti_in_blocklist(token_data['jti']):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
                "message": "Token has expired or revoked.",
                "comments": "Please get new token." 
            }) 

        self.verify_token_data(token_data=token_data)

        return token_data

        
    def token_valid(self, token:str) -> dict | None:
        token_data = decode_token(token=token)
        return token_data if token_data is not None else None

    def verify_token_data(self, token_data):
        raise NotImplemented("Please override this method.")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data:dict):
        if token_data and token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Please provide a access token.")

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data:dict):
        if token_data and not token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Please provide a refresh token.")


async def get_current_user(userData:dict=Depends(AccessTokenBearer()), session:AsyncSession=Depends(get_session)):
    email = userData['user']['email']
    user = await userServices.get_user_by_email(email=email, session=session)
    return user

class RoleChecker:
    def __init__(self, allowedRoles:List[str]):
        self.allowedRoles = allowedRoles

    def __call__(self, user:User = Depends(get_current_user)):
        if user.role in self.allowedRoles:
            return True
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User is not authorized to perform this action.")