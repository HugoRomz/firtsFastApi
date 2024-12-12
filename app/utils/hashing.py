from fastapi import HTTPException, status
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    try:
        if pwd_context.identify(password) == "bcrypt":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña ya está encriptada")
        
        return pwd_context.hash(password)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al encriptar la contraseña") from e

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al verificar la contraseña") from e
