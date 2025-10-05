from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class Book(BaseModel):
    id: UUID
    title: str
    author: str
    page_count: int
    language: str
    publisher: str
    published_date: str
    created_at: datetime
    updated_at: datetime

class BookCreateModel(BaseModel):
    title: str
    author: str
    page_count: int
    language: str
    publisher: str
    published_date: str


class BookUpdateModel(BaseModel):
    title: str
    author: str
    page_count: int
    language: str
    publisher: str

