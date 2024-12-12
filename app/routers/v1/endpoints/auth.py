from fastapi import APIRouter, HTTPException, status
from app.services.auth import create_user, login_user, logout_user
from app.schemas.user import UserCreate, UserOut, UserLogin, UserToken

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}},
)

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    return await create_user(user)

@router.post("/login")
async def login(user: UserLogin):
    return await login_user(user)

@router.post("/logout")
async def logout(user: UserToken):
    return await logout_user(user)
