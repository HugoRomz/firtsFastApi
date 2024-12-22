# routers/v1/endpoints/denue.py
from fastapi import APIRouter, Query, HTTPException
from app.services.denueapi import buscar_empresa_en_denue

router = APIRouter()

@router.get("/buscar")
async def buscar_establecimientos(
    nombre: str = Query(..., description="Palabras clave a buscar o 'todos'"),
    entidad: str = Query("00", description="Clave de la entidad federativa (01-32 o '00' para todas)"),
    registro_inicial: int = Query(1, description="Número de registro inicial"),
    registro_final: int = Query(50, description="Número de registro final")
):

    try:
        resultado = await buscar_empresa_en_denue(nombre, entidad, registro_inicial, registro_final)
        if not resultado:
            raise HTTPException(status_code=404, detail="No se encontraron resultados en DENUE")
        return {"message": "Búsqueda exitosa", "data": resultado}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {e}")
