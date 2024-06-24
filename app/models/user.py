from typing import Optional

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: str = Field(unique=True)
    username: str = Field(unique=True)
    first_name: str
    last_name: str


class User(UserBase, table=True):
    __tablename__ = "user"

    id: int = Field(default=None, primary_key=True, index=True)
    is_staff: bool = Field(default=False)
    is_admin: bool = Field(default=False)
    balance: float = Field(default=0.0)
    age: int = Field(default=None)


class UserCreate(UserBase):
    ...


class UserUpdate(UserBase):
    ...

