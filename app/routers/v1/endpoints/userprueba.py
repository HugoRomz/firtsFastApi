from typing import List
from fastapi import APIRouter, Depends
from app.schemas.user import UserOut
from app.db.client import db

router = APIRouter()

# RUTA NO PROTEGIDA PARA OBETENER TODOS LOS USUARIOS, SOLO PARA PRUEBAS
@router.get("/users", response_model=List[UserOut])
async def get_users():
    users = await db["users"].find().to_list(length=None)
    print(users)
    return [UserOut(id=str(u["_id"]), **u) for u in users]
