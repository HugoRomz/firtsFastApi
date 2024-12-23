# app/routers/v1/roles.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.user import UserUpdate, UserComplete
from app.services.user import list_users, get_user_by_id, handle_complete_user, deactivate_user, update_user_role
from app.dependencies.auth import get_current_user
from app.middleware.verify_role import verify_role

router = APIRouter()

@router.get("/users")
async def get_all_users(skip: int = 0, limit: int = 10, current_user=Depends(verify_role("Wooper"))):
   return await list_users(skip=skip, limit=limit)

@router.get("/users/{id}")
async def get_user(id: str, current_user=Depends(get_current_user)):
    return await get_user_by_id(id)

@router.patch("/complete/{id}")
async def complete_user(id: str, user_data: UserComplete, current_user=Depends(verify_role("Wooper"))):
    return await handle_complete_user(id, user_data)

@router.delete("/users/{id}")
async def delete_user(id: str, current_user=Depends(verify_role("Wooper"))):
    return await deactivate_user(id)

@router.post("/users/{id}/avatar")
async def upload_avatar(id: str, current_user=Depends(get_current_user)):
    return "Subir/actualizar foto de perfil."

@router.post("/users/{id}/cover")
async def upload_cover_photo(id: str, current_user=Depends(get_current_user)):
    return "Subir/actualizar foto de portada."

@router.put("/users/role/{id}")
async def update_role(user_id: str, role_id: str, current_user=Depends(get_current_user)):
    return await update_user_role(user_id, role_id)


