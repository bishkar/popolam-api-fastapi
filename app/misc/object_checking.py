from abc import ABC, abstractmethod
from fastapi import Request

from fastapi import Request
from sqlmodel import select

from app.models import Product, User


class Checker(ABC):
    @abstractmethod
    async def check(self, request: Request) -> bool:
        pass


class ObjectChecker(Checker):
    __checker__ = None

    @classmethod
    def set_checker(cls, checker):
        cls.__checker__ = checker
    
    @staticmethod
    async def check(request: Request) -> bool:
        return await ObjectChecker.__checker__.check(request)    


class ProductChecker(Checker):
    @staticmethod
    async def check(request: Request) -> bool:
        match request.method:
            case "POST":
                body = await request.json()
                statement = select(Product).where(Product.name == body.get('name'))
            case _:
                statement = select(Product).where(Product.id == int(request.path_params['unique_id']))
        result = await request.state.db.execute(statement)
        product = result.scalars().first()
        return product is not None
    

class UserChecker(Checker):
    @staticmethod
    async def check(request: Request) -> bool:
        match request.method:
            case "POST":
                body = await request.json()
                statement = select(User).where(User.username == body.get('username')
                                            or User.email == body.get('email'))
            case _:
                statement = select(User).where(User.id == int(request.path_params['unique_id']))
        result = await request.state.db.execute(statement)
        user = result.scalars().first()
        return user is not None
    