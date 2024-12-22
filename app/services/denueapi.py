# services/denue.py
import httpx
from fastapi import HTTPException
from app.core.config import settings

DENUE_API_KEY = settings.DENUE_API_KEY
DENUE_API_URL = settings.DENUE_API_URL

async def buscar_empresa_en_denue(
    nombre: str,
    entidad: str = "00",
    registro_inicial: int = 1,
    registro_final: int = 50
):

    if not DENUE_API_KEY or not DENUE_API_URL:
        raise HTTPException(status_code=500, detail="Faltan configuraciones de DENUE en .env")

    # Construimos la URL según el formato necesario
    url = (
        f"{DENUE_API_URL}/consulta/Nombre/{nombre}/{entidad}/{registro_inicial}/{registro_final}/{DENUE_API_KEY}"
    )

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=503,
                detail=f"Error de conexión con la API DENUE: {exc}"
            )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Error al consultar la API de DENUE: {response.text}"
        )

    return response.json()
