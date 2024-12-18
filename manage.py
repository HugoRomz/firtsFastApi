# manage.py
import asyncio
import typer
from app.db.client import db  # Importa db desde tu aplicación
from bson import ObjectId

app = typer.Typer()

initial_roles = [
    {"name": "Wooper", "description": "Proveedor de servicios", "type": "public"},
    {"name": "Cliente", "description": "Consumidor de servicios", "type": "public"},
    {"name": "Empresa", "description": "Organización proveedora", "type": "public"},
    {"name": "Administrador", "description": "Todos los privilegios", "type": "internal"},
    {"name": "Programador", "description": "Mantenimiento interno", "type": "internal"},
]

@app.command()
def seed():

    async def _seed():
        for r in initial_roles:
            existing = await db["roles"].find_one({"name": r["name"]})
            if not existing:
                await db["roles"].insert_one(r)
        print("Seeding completo.")

    asyncio.run(_seed())

if __name__ == "__main__":
    app()
