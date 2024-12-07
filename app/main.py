from fastapi import FastAPI
from routers.v1.endpoints import auth, db_test
from core.config import settings

app = FastAPI(title=settings.PROJECT_NAME,version=settings.VERSION)


app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(db_test.router, prefix="/api/v1", tags=["DB Test"])

@app.get("/")
async def root():
    return "Root de Login"



