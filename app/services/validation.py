from fastapi import HTTPException,status
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def validate_passwords(password: str, confirm_password: str): 
    if password != confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Las contraseñas no coinciden")
    if len(password) < 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña debe tener al menos 8 caracteres")
    if len(password) > 50:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no puede tener más de 50 caracteres")
    if not any(char.isdigit() for char in password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña debe contener al menos un número")
    if not any(char.isalpha() for char in password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña debe contener al menos una letra")
    if not any(char.isupper() for char in password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña debe contener al menos una letra mayúscula")
    if not any(char.islower() for char in password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña debe contener al menos una letra minúscula")
    if not any(char in ['!', '@', '#', '$', '%', '&', '*','.'] for char in password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña debe contener al menos un caracter especial (!, @, #, $, %, &, *)")

def get_password_hash(password):
    try:
        return pwd_context.hash(password)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al encriptar la contraseña") from e

def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al verificar la contraseña") from e
    
