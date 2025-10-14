from passlib.context import CryptContext

password_context = CryptContext(
    schemes=['bcrypt']
)

def generate_password_hash(password: str) -> str:
    hashed_pass = password_context.hash(password)
    return hashed_pass

def verify_password(password: str, hash: str) -> bool:
    result = password_context.verify(secret=password, hash=hash)
    return result