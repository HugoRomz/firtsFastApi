from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from app.schemas.roles import RoleOut
from app.schemas.user import UserCreate, UserLogin, UserOut, UserToken
from app.services.auth import create_user, login_user, logout_user, get_public_roles
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    return await create_user(user)

@router.post("/login")
async def login(user: UserLogin):
    return await login_user(user)


@router.post("/logout")
async def logout(user: UserToken = Depends(get_current_user)):
    return await logout_user(user)


@router.get("/me", response_model=UserOut)
async def get_me(current_user: UserOut = Depends(get_current_user)):
    return current_user

@router.get("/roles", response_model=List[RoleOut])
async def get_roles():
    roles = await get_public_roles()
    return roles