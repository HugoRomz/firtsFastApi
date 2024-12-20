from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from app.schemas.roles import RoleOut
from app.schemas.auth import RegisterSchema, LoginSchema, TokenResponseSchema, RegisterOut
from app.schemas.user import UserOut
from app.services.auth import register_user, login_user, logout_user, get_public_roles
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.post("/register", response_model=RegisterOut)
async def register(user: RegisterSchema):
    return await register_user(user)

@router.post("/login")
async def login(user: LoginSchema):
    return await login_user(user)


@router.post("/logout")
async def logout(user: TokenResponseSchema = Depends(get_current_user)):
    return await logout_user(user)


@router.get("/me", response_model=UserOut)
async def get_me(current_user: UserOut = Depends(get_current_user)):
    return current_user

@router.get("/roles", response_model=List[RoleOut])
async def get_roles():
    roles = await get_public_roles()
    return roles