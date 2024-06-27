from fastapi import Depends, APIRouter, HTTPException, Request
from typing import List, Optional, Annotated
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.api.routes.auth import get_current_user
from app.crud.user import UserCRUD, UserCreate, UserUpdate
from app.misc.jwt_helpers import verify_token
from app.models import User, UserPreview
from app.dependencies import get_db
from app.misc import ObjectChecker, UserChecker


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/{unique_id}")
async def get_user(
    unique_id: int, 
    db_session: Annotated[AsyncSession, Depends(get_db)]
) -> Optional[UserPreview]:
    crud = UserCRUD()
    return await crud.retrieve(unique_id, db_session)

@router.get("/")
async def get_users(
    db_session: Annotated[AsyncSession, Depends(get_db)]
) -> List[UserPreview]:
    crud = UserCRUD()
    return await crud.get(db_session)

@router.post("/")
async def create_user(
    user: UserCreate,
    request: Request,
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    crud = UserCRUD()
    ObjectChecker.set_checker(UserChecker)

    is_exist = await ObjectChecker.check(request)
    return await crud.create(user, db_session, is_exist)

@router.delete("/{unique_id}", description="Add user to blacklist")
async def add_to_blacklist(
    unique_id: int,
    request: Request,
    db_session: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)]
) -> None:
    if not user.is_staff:
        raise HTTPException(status_code=403, detail="You are not allowed to perform this action")
    
    crud = UserCRUD()
    ObjectChecker.set_checker(UserChecker)
    
    is_exist = await ObjectChecker.check(request)
    return await crud.delete(unique_id, db_session, is_exist)

@router.put("/{unique_id}")
async def make_staff(
    unique_id: int,
    request: Request,
    db_session: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    data: UserUpdate
) -> None:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="You are not allowed to perform this action")
    
    crud = UserCRUD()
    ObjectChecker.set_checker(UserChecker)
    
    is_exist = await ObjectChecker.check(request)
    return await crud.update(unique_id, data, db_session, is_exist
)
