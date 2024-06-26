from typing import Any, Dict, Optional, Tuple
from passlib.context import CryptContext
from sqlmodel import Field, SQLModel, select


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserBase(SQLModel):
    email: str = Field(unique=True)
    username: str = Field(unique=True)
    first_name: str 
    last_name: str
    age: int = Field(default=None)


class User(UserBase, table=True):
    __tablename__ = "user"

    id: int = Field(default=None, primary_key=True, index=True)
    is_staff: bool = Field(default=False)
    is_admin: bool = Field(default=False)
    balance: float = Field(default=0.0)
    password: str = Field(default=None)
    on_blacklist: bool = Field(default=False)

    def set_password(self, password: str) -> None:
        self.password = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password)


class UserCreate(UserBase):
    password: str = Field(default=None)


class UserUpdate(SQLModel):
    is_staff: bool


class UserLogin(SQLModel):
    username: str
    password: str


class UserPreview(SQLModel):
    id: int
    username: str
    is_staff: bool
    is_admin: bool
    balance: float
    age: int
    