from fastapi import Depends, APIRouter
from typing import Optional, Annotated
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


from app.crud.user import UserCRUD
from app.models import User
from app.dependencies import get_db, user_exists


@router.get("/user/{unique_id}")
async def get_user(
    unique_id: int, 
    db_session: Annotated[AsyncSession, Depends(get_db)]
) -> Optional[User]:
    crud = UserCRUD()
    return await crud.retrieve(unique_id, db_session)

@router.get("/user")
async def get_user(
    db_session: Annotated[AsyncSession, Depends(get_db)]
) -> list[User]:
    crud = UserCRUD()
    return await crud.get(db_session)

@router.post("/user")
async def create_user(
    user: User,
    db_session: Annotated[AsyncSession, Depends(get_db)],
    is_exist: Annotated[bool, Depends(user_exists)]
) -> User:
    crud = UserCRUD()
    return await crud.create(user, db_session, is_exist)

@router.delete("/user/{unique_id}")
async def delete_user(
    unique_id: int,
    db_session: Annotated[AsyncSession, Depends(get_db)],
    is_exist: Annotated[bool, Depends(user_exists)]
) -> None:
    crud = UserCRUD()
    return await crud.delete(unique_id, db_session, is_exist)
