from fastapi import APIRouter, HTTPException, status
from services.auth import create_user, verify_user
from models.user import UserCreate, UserOut, UserLogin
from db.client import db 

router = APIRouter(responses={status.HTTP_404_NOT_FOUND: {"message":"No encontrado"}})

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):

    existing_user = await db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El email ya está registrado")
        
    new_user_id = await create_user(user)

    # Retornar el usuario registrado (sin contraseña)
    return {
        "id": str(new_user_id),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone_number": user.phone_number,
        "gendered": user.gendered,
        "is_active": True
    }

@router.post("/login", response_model=UserOut)
async def login(user: UserLogin):
    db_user = await verify_user(user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Credenciales incorrectas")
    return {
        "id": str(db_user["_id"]),
        "first_name": db_user["first_name"],
        "last_name": db_user["last_name"],
        "email": db_user["email"],
        "phone_number": db_user["phone_number"],
        "gendered": db_user["gendered"],
        "is_active": db_user["is_active"]
    }