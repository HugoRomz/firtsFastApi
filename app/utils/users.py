from app.db.client import db

def search_user(field: str, key):
    try:
        user = db["users"].find_one({field: key})
        return user
    except:
        return {"Error": "No se ha encontrado el usuario"}
