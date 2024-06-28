from sqlmodel import Field, SQLModel


class Order(SQLModel, table=True):
    __tablename__ = "order"

    id: int = Field(default=None, primary_key=True, index=True)
    customer: int = Field(default=None, foreign_key="user.id")
    product: int = Field(default=None, foreign_key="product.id")
    quantity: int = Field(default=0)
    is_paid: bool = Field(default=False)


class OrderCreate(SQLModel):
    customer: int
    product: int
    quantity: int
