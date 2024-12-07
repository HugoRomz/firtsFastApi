from fastapi import APIRouter, HTTPException
from db.client import db

router = APIRouter()

@router.get("/test-db")
async def test_db_connection():
    try:
        await db.command("ping")
        return {"status": "Connected", "message": "La conexión a la base de datos fue exitosa"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión a la base de datos: {str(e)}")