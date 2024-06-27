from typing import Optional
from sqlmodel import Field, SQLModel


class Product(SQLModel, table=True):
    __tablename__ = "product"

    id: int = Field(default=None, primary_key=True, index=True)
    name: str = Field(max_length=100, unique=True)
    description: str = Field(max_length=1000)
    price: float = Field(default=0.0)
    popularity: int = Field(default=1, ge=1, le=5)


class ProductCreate(SQLModel):
    name: str
    description: str
    price: float
    popularity: int


class ProductUpdate(SQLModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    popularity: Optional[int]
