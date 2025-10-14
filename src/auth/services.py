#     async def create_user(self, userData: UserCreateModel, session: AsyncSession):
#         user_data_dict = userData.model_dump(exclude={"password"})
#         new_user = User(
#             **user_data_dict,
#             password_hash = generate_password_hash(userData.password)
#         )
#         session.add(new_user)
#         await session.commit()
#         return new_user 


from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models.models import User
from schemas.users import UserCreateModel
from .utils import generate_password_hash, verify_password

class UserServices:
    async def get_user_by_email(self, email:str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement=statement)
        user = result.one_or_none()
        return user if user is not None else None

    async def check_user_exits(self, email:str, session: AsyncSession) -> bool:
        user = await self.get_user_by_email(email=email, session=session)
        return True if user is not None else False

    async def create_user(self, userData:UserCreateModel, session:AsyncSession):
        user_data_dict = userData.model_dump()
        user = User(
            **user_data_dict,
            password_hash=generate_password_hash(userData.password)
        )
        session.add(user)
        await session.commit()
        return user