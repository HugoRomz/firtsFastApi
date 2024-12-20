from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.user import UserOut
from app.dependencies.auth import get_current_user
from app.db.client import db

router = APIRouter()

@router.get("/users", response_model=List[UserOut])
async def get_all_users(skip: int = 0, limit: int = 10, current_user=Depends(get_current_user)):
    users = await db["users"].find().skip(skip).limit(limit).to_list(limit)
    return [UserOut(id=str(u["_id"]), **u) for u in users]

