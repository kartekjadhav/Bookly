from datetime import datetime
from sqlalchemy.ext.asyncio.session import AsyncSession
from schemas.schemas import BookCreateModel, BookUpdateModel
from sqlmodel import select, desc
from models.models import Book

class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.execute(statement=statement)
        return result.scalars().all()
    
    async def get_a_book(self, book_uid:str, session: AsyncSession):
        statement = select(Book).where(Book.id == book_uid)
        result = await session.execute(statement=statement)
        book = result.scalars().first()

        return book if book is not None else None

    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        book_data_dict = book_data.model_dump()
        new_book = Book(
            **book_data_dict
        )

        new_book.published_date = datetime.strptime(book_data_dict["published_date"], "%Y-%m-%d")

        session.add(new_book)
        await session.commit()

        return new_book

    async def update_book(self, book_uid: str, update_data: BookUpdateModel, session: AsyncSession):
        book_to_update = await self.get_a_book(book_uid, session)

        if update_data is None:
            return None
        else:
            for k, v in update_data.model_dump().items():
                setattr(book_to_update, k, v)
            await session.commit()
            return book_to_update

    async def delete_book(self, book_uid: str, session: AsyncSession):
        book_to_delete = await self.get_a_book(book_uid=book_uid, session=session)

        if book_to_delete is None:
            return None
        else:
            await session.delete(book_to_delete)
            await session.commit()
            return {}
