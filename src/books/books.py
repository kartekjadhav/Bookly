from typing import List, Dict
from fastapi import APIRouter, status, Depends, HTTPException
from schemas.schemas import Book, BookCreateModel, BookUpdateModel
from .services import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from db.main import get_session
from src.auth.dependencies import AccessTokenBearer, RoleChecker


bookRouter = APIRouter()
bookService = BookService()
access_token_bearer = AccessTokenBearer()
roleChecker = Depends(RoleChecker(['admin', 'user']))


# Get all books
@bookRouter.get("/", status_code=status.HTTP_200_OK, response_model=List[Book], dependencies=[roleChecker])
async def get_all_books(session: AsyncSession = Depends(get_session), user_details=Depends(access_token_bearer)):
    print(user_details)
    books = await bookService.get_all_books(session=session)
    return books

# Create a book
@bookRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Book, dependencies=[roleChecker])
async def create_book(book_data: BookCreateModel, 
                        session: AsyncSession = Depends(get_session), user_details=Depends(access_token_bearer)
                    ):
    try:
        new_book = await bookService.create_book(book_data=book_data, session=session)
        return new_book
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error in creating book: {e}")


# Get a book
@bookRouter.get("/{book_uid}", response_model=Book, status_code=status.HTTP_200_OK, dependencies=[roleChecker])
async def get_a_book(book_uid: str, session: AsyncSession = Depends(get_session), user_details=Depends(access_token_bearer)):
    book = await bookService.get_a_book(book_uid=book_uid, session=session)
    if book:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_uid} not found"
        )

@bookRouter.patch("/{book_uid}", status_code=status.HTTP_200_OK, response_model=Book, dependencies=[roleChecker])
async def update_book(book_uid: str,
                      update_data: BookUpdateModel,
                      session: AsyncSession = Depends(get_session), user_details=Depends(access_token_bearer)
                ) -> dict:
    try:
        update_book = await bookService.update_book(
            book_uid=book_uid, 
            update_data=update_data,
            session=session
        )

        if update_book is not None:
            return update_book
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_uid} not found"
            )

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error in updating book: {e}")

@bookRouter.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[roleChecker])
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session), user_details=Depends(access_token_bearer)):
    try:
        book_to_delete = await bookService.delete_book(
            book_uid=book_uid,
            session=session
        )

        if book_to_delete is not None:
            return {}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_uid} not found"
            )

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error in deleting book: {e}")