from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.v1.endpoints import auth, db_test, roles, tianguis, users
from app.core.config import settings


def create_app():
    app = FastAPI(title=settings.PROJECT_NAME,version=settings.VERSION)

    origins = [
        settings.URL_FRONTEND,
        "http://localhost",
        "http://localhost:3000"
    ]
    
    app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

    app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
    app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
    app.include_router(db_test.router, prefix="/api/v1", tags=["DB Test"])
    app.include_router(roles.router, prefix="/api/v1/roles", tags=["Roles"])
    app.include_router(tianguis.router, prefix="/api/v1/tianguis", tags=["Tianguis"])


    

    return app

app = create_app()

@app.get("/")
async def root():
    return "Root"



