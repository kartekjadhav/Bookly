from datetime import date, datetime
from pydantic import BaseModel
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg 
from typing import Optional, List


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
    user_uid: Optional[UUID] = Field(
        default=None, 
        foreign_key="users.uid"
    )
    user: Optional["User"] = Relationship(back_populates="books")
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
    role: str = Field(sa_column=Column(pg.VARCHAR ,nullable=False, server_default='user'))
    password_hash: str = Field(sa_column=Column(pg.VARCHAR, nullable=False), exclude=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    books: Optional[List["Book"]] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy":"selectin"})

    def __repr__(self):
        return f"<User {self.username}>"
    
