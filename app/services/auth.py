from app.db.client import db
from datetime import datetime
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.utils.hashing import get_password_hash, verify_password
from app.utils.jwt import create_access_token
from app.utils.validation import validate_passwords
from app.utils.roles import verify_role_exists
from bson import ObjectId
from fastapi import HTTPException, status


async def create_user(user: UserCreate) -> UserOut:
    # Validar si el usuario existe
    existing_user = await db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya existe.",
        )

    # Validar contraseñas y hashear
    validate_passwords(user.password, user.confirm_password)
    hashed_password = get_password_hash(user.password)

    # Crear usuario en la base de datos
    user_data = user.model_dump()

    if user_data.get("date_of_birth"):
        user_data["date_of_birth"] = datetime.combine(user_data["date_of_birth"], datetime.min.time())

    # AGREGAR ROL
    if user_data.get("role_id"):
        role = await verify_role_exists(user_data["role_id"])
        user_data["role_id"] = role["_id"]  
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El rol es requerido.",
        )
    
    user_data["hashed_password"] = hashed_password
    del user_data["password"], user_data["confirm_password"]

    result = await db["users"].insert_one(user_data)
    return UserOut(id=str(result.inserted_id), **user.model_dump())


async def login_user(user: UserLogin):
    # Validar usuario
    db_user = await db["users"].find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas"
        )

    token = create_access_token({"sub": db_user["email"], "id": str(db_user["_id"])})
    
    await db["users"].update_one({"_id": db_user["_id"]}, {"$set": {"user_token": token}})
    return {"access_token": token, "token_type": "bearer"}

async def logout_user(user: UserOut):
    await db["users"].update_one({"_id": ObjectId(user.id)}, {"$set": {"user_token": None}})
    return {"message": "Sesión cerrada exitosamente."}
