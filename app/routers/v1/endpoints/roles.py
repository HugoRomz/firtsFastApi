# app/routers/v1/roles.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.roles import RoleCreate, RoleUpdate, RoleOut
from app.services.role import create_role, get_role_by_id, list_roles, update_role, delete_role
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=RoleOut)
async def create_new_role(role_data: RoleCreate, ):
    return await create_role(role_data)

@router.get("/", response_model=List[RoleOut])
async def get_all_roles(skip: int = 0, limit: int = 10, current_user=Depends(get_current_user)):
    return await list_roles(skip=skip, limit=limit)

@router.get("/{role_id}", response_model=RoleOut)
async def get_one_role(role_id: str, current_user=Depends(get_current_user)):
    return await get_role_by_id(role_id)

@router.put("/{role_id}", response_model=RoleOut)
async def update_existing_role(role_id: str, role_data: RoleUpdate, current_user=Depends(get_current_user)):
    return await update_role(role_id, role_data)

@router.delete("/{role_id}")
async def remove_role(role_id: str, current_user=Depends(get_current_user)):
    return await delete_role(role_id)
