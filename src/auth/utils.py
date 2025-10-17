import jwt
from uuid import uuid4
from passlib.context import CryptContext
from datetime import timedelta, datetime
import logging

from config.config import Config
from schemas.users import UserLoginModel

ACCESS_TOKEN_EXPIRY = 3600

password_context = CryptContext(
    schemes=['bcrypt']
)

def generate_password_hash(password: str) -> str:
    hashed_pass = password_context.hash(password)
    return hashed_pass

def verify_password(password: str, hash: str) -> bool:
    result = password_context.verify(secret=password, hash=hash)
    return result

def create_access_token(userData: dict, expiry:timedelta=None, refresh:bool=False):
    payload = {}
    payload['user'] = userData
    expiry_time = datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['exp'] = int(expiry_time.timestamp())
    payload['jti'] = str(uuid4())
    payload['refresh'] = refresh

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )

    return token

def verify_access_token(token:str):
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )

        return token_data
    except jwt.exceptions.PyJWTError as e:
        logging.exception(e)
        return None

