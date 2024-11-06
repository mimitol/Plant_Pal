from fastapi import APIRouter, Response, HTTPException
from DB.DB_patterns import User
from Logic.CRUD import user_crud
from exceptions import exceptions_handler


router = APIRouter()


# קבלת כל המשתמשים
@router.get('/plantpal/users')
async def get_all_users():
    try:
        users = await user_crud.get_all_users()
        return users
    except Exception as ex:
        return exceptions_handler(ex)


# קבלת משתמש לפי מייל
@router.get('/plantpal/user/{email}')
async def get_user(email: str):
    try:
        user = await user_crud.get_user(email)
        return user
    except Exception as ex:
        return exceptions_handler(ex)


# הוספת משתמש
@router.post('/plantpal/user')
async def add_user(user: User):
    try:
        result = await user_crud.add_user(user)
        return result
    except Exception as ex:
        return exceptions_handler(ex)


# בדיקת סיסמא של משתמש שמתחבר
@router.post('/plantpal/user/login/{email}')
async def check_password(email: str, data: dict):
    try:
        password = data.get('password')
        result = await user_crud.check_password(email, password)
        return result
    except Exception as ex:
        return exceptions_handler(ex)


# עדכון פרטי משתמש
@router.put('/plantpal/user/{email}')
async def update_user(email: str, user_data: User):
    try:
        updated_user = await user_crud.update_user(email, user_data)
        return updated_user
    except Exception as ex:
        return exceptions_handler(ex)


# מחיקת משתמש
@router.delete('/plantpal/user/{email}')
async def delete_user(email):
    try:
        result = await user_crud.delete_user(email)
        return result
    except Exception as ex:
        return exceptions_handler(ex)











