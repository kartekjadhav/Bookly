from datetime import date, datetime
from pydantic import BaseModel
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg 

class Book(SQLModel, table=True):
    __tablename__ = "books"

    id: UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            default=uuid4,
            nullable=False
        )
    )
    title: str
    author: str
    page_count: int
    language: str
    publisher: str
    published_date: date
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP ,default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f"<Book {self.title}>"



class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: UUID = Field(sa_column=Column(
        pg.UUID,
        default=uuid4,
        primary_key=True,
        nullable=False,
    ))
    username: str
    first_name: str
    last_name: str
    email: str
    verified: bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f"<User {self.username}>"
