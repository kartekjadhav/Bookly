from typing import List, Dict
from fastapi import APIRouter, status, Depends, HTTPException
from schemas.schemas import Book, BookCreateModel, BookUpdateModel
from .services import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from db.main import get_session

bookRouter = APIRouter()
bookService = BookService()

# Get all books
@bookRouter.get("/", status_code=status.HTTP_200_OK, response_model=List[Book])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    books = await bookService.get_all_books(session=session)
    return books

# Create a book
@bookRouter.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book_data: BookCreateModel, 
                        session: AsyncSession = Depends(get_session)
                    ):
    try:
        new_book = await bookService.create_book(book_data=book_data, session=session)
        return new_book
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error in creating book: {e}")


# Get a book
@bookRouter.get("/{book_uid}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_a_book(book_uid: int, session: AsyncSession = Depends(get_session)):
    book = await bookService.get_a_book(book_uid=book_uid, session=session)
    if book:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_uid} not found"
        )

@bookRouter.patch("/{book_uid}", status_code=status.HTTP_200_OK)
async def update_book(book_uid: int,
                      update_data: BookUpdateModel,
                      session: AsyncSession = Depends(get_session)
                ) -> dict:
    try:
        update = await bookService.update_book(
            book_uid=book_uid, 
            update_data=update_data,
            session=session
        )

        if update is not None:
            return update
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_uid} not found"
            )

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error in updating book: {e}")

@bookRouter.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def get_all_books(book_uid: int, session: AsyncSession = Depends(get_session)):
    try:
        book_to_delete = await bookService.delete_book(
            book_uid=book_uid,
            session=session
        )

        if book_to_delete is not None:
            return None

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_uid} not found"
            )

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error in deleting book: {e}")