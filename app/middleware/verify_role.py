from fastapi import Depends, HTTPException, status
from bson import ObjectId
from app.db.client import db
from app.schemas.user import UserOut
from app.dependencies.auth import get_current_user

def verify_role(required_role: str):
    async def wrapper(current_user: UserOut = Depends(get_current_user)):
        if not current_user.role_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario sin rol asignado."
            )

        role = await db["roles"].find_one({"_id": ObjectId(current_user.role_id)})
        
        if "Administrador" in role.get("name"):
            return current_user
            
        if not role or role.get("name") != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere el rol '{required_role}'."
            )

        return current_user
    return wrapper