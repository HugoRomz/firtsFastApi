from fastapi import HTTPException, status
from pymongo.errors import PyMongoError
from app.core.config import settings
from app.db.client import db
from datetime import datetime, timedelta
from app.schemas.user import UserCreate, UserOut, UserLogin, UserToken
from app.models.user import UserInDB
from app.utils.hashing import get_password_hash, verify_password
from app.utils.validation import validate_passwords
from app.utils.users import search_user
from app.utils.jwt import create_access_token, verify_token
from bson import ObjectId 

async def create_user(user: UserCreate) -> UserOut:
    # user exist 
    if await search_user("email", user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya existe",
        )

    # Hash de contraseñas
    validate_passwords(user.password, user.confirm_password)
    hashed_password = get_password_hash(user.password)

    # Se crea un objeto UserInDB con los datos del usuario a insertar
    user_data = UserInDB(
        first_name=user.first_name,
        last_name=user.last_name,
        date_of_birth=user.date_of_birth,
        gendered=user.gendered,
        email=user.email,
        phone_number=user.phone_number,
        hashed_password=hashed_password,
        user_token=None,
    )

    # Se convierte el objeto UserInDB a un diccionario porque PyMongo no acepta objetos
    user_dict = user_data.model_dump()
    if user_dict.get("date_of_birth"):
        user_dict["date_of_birth"] = datetime.combine(user_dict["date_of_birth"], datetime.min.time())

    # Insercion de MongoDB 
    result = await db["users"].insert_one(user_dict)

    # formato de salida 
    return UserOut(
        id=str(result.inserted_id),
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone_number=user.phone_number,
        is_active= True,

    )

async def login_user(user: UserLogin) -> UserOut:
    # Verificar usuario
    user_data = await verify_user(user.email, user.password)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user_data.email}, expires_delta=access_token_expires)

    user_id = ObjectId(user_data.id)  # Convertir _id de cadena a ObjectId
    
    # Actualizar token en la base de datos
    await db["users"].update_one({"_id": user_id}, {"$set": {"user_token": access_token}})
    

    return {"access_token": access_token, "token_type": "bearer", "user": user_data}

async def logout_user(user: UserToken) -> dict:
    try:
        # Verificar el token del usuario
        payload = verify_token(user.token)
        
        # Validar que el usuario exista en la base de datos
        user_id = ObjectId(user.user_id)
        user_in_db = await db["users"].find_one({"_id": user_id})
        if not user_in_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado.",
            )
        
        # Eliminar el token del usuario en la base de datos
        await db["users"].update_one({"_id": user_id}, {"$set": {"user_token": None}})
        return {"message": "Sesión cerrada exitosamente."}
    
    except HTTPException as http_exc:
        raise http_exc  # Re-raise HTTPException para errores de token
    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la base de datos: {str(e)}"
        )


async def verify_user(email: str, password: str) -> UserOut:
    try:
        # Buscar usuario en la base de datos
        user = await db["users"].find_one({"email": email})

        # Validar existencia del usuario
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="El usuario o la contraseña son incorrectos."
            )

        # Validar contraseña
        if not verify_password(password, user.get("hashed_password", "")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="El usuario o la contraseña son incorrectos."
            )

        # Verificar que el usuario esté activo
        if not user.get("is_active", False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El usuario está inactivo. Contacte al administrador."
            )

        return UserOut(
            id=str(user["_id"]),
            first_name=user["first_name"],
            last_name=user["last_name"],
            email=user["email"],
            phone_number=user.get("phone_number"),
            date_of_birth=user.get("date_of_birth"),
            gendered=user.get("gendered"),
            is_active=user["is_active"],
        )
    except PyMongoError as e:
        # Manejar errores específicos de MongoDB
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la base de datos: {str(e)}"
        )