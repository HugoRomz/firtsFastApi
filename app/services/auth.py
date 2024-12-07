from db.client import db
from datetime import datetime
from models.user import UserCreate, UserInDB
from services.validation import validate_passwords,get_password_hash, verify_password


async def create_user(user: UserCreate):
    
    validate_passwords(user.password, user.confirm_password)

    hashed_password = get_password_hash(user.password)

    user_data = UserInDB(
        first_name=user.first_name,
        last_name=user.last_name,
        date_of_birth=user.date_of_birth,
        gendered=user.gendered,
        email=user.email,
        phone_number=user.phone_number,
        hashed_password=hashed_password
    )
    user_dict = dict(user_data)
    if user_dict.get("date_of_birth"):
        user_dict["date_of_birth"] = datetime.combine(user_dict["date_of_birth"], datetime.min.time())

    result = await db["users"].insert_one(user_dict)

    return result.inserted_id

async def verify_user(email: str, password: str):
    user = await db["users"].find_one({"email": email})
    if not user:
        return False
    if not user.get("is_active"):
        return False
    if not verify_password(password, user.get("hashed_password")):
        return False
    return user
    