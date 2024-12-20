# app/routers/v1/roles.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.dependencies.auth import get_current_user
from app.middleware.verify_role import verify_role

router = APIRouter()

@router.get("/users")
async def get_all_users(skip: int = 0, limit: int = 10, current_user=Depends(get_current_user)):
    return "Listar usuarios (con paginación y filtros opcionales)."

@router.get("/users/{id}")
async def get_user(id: str, current_user=Depends(get_current_user)):
    return "Obtener detalles de un usuario específico."

@router.patch("/users/{id}")
async def update_user(id: str, current_user=Depends(get_current_user)):
    return "Actualizar perfil de usuario."

@router.delete("/users/{id}")
async def delete_user(id: str, current_user=Depends(get_current_user)):
    return "Eliminar usuario."

@router.post("/users/{id}/avatar")
async def upload_avatar(id: str, current_user=Depends(get_current_user)):
    return "Subir/actualizar foto de perfil."

@router.post("/users/{id}/cover")
async def upload_cover_photo(id: str, current_user=Depends(get_current_user)):
    return "Subir/actualizar foto de portada."


