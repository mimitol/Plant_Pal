from DB import DB_access
import pyodbc
from DB.DB_patterns import User

from exceptions import  InvalidSignupError, InvalidLoginError


async def get_all_users():
    query="SELECT * FROM Users"
    users = await DB_access.execute_query(query)
    return users


async def add_user(user: User):
    exist = await DB_access.execute_query("SELECT * FROM Users WHERE email =?;", user.email)
    if not exist:
        new_user = (user.user_name, user.password, user.email, user.watering_hours, user.interested_in_reminders,
                    user.token_for_reminders)
        query = "INSERT INTO Users (user_name,password,email, watering_hours, interested_in_reminders,token_for_notifications) VALUES (?, ?, ?, ?,?,?);"
        await DB_access.execute_query(query, new_user)
        res = await DB_access.execute_query("SELECT * FROM Users WHERE email=?", (user.email))
        return res
    else:
        raise InvalidSignupError


async def delete_user(email):
    query = "DELETE FROM Users WHERE email= ?;"
    res = await DB_access.execute_query(query, email)
    return res

async def get_user(email):
    query = "SELECT * FROM Users WHERE email= ?;"
    res = await DB_access.execute_query(query, email)
    return res


async def update_user(email, user: User):
    updated_user = (
    user.user_name, user.password, user.watering_hours, user.interested_in_reminders, user.token_for_reminders, email)
    query = "UPDATE Users SET user_name=? password=?, watering_hours=?, interested_in_reminders=?, token_for_reminders = ? WHERE email = ?;"
    res = await DB_access.execute_query(query, updated_user)
    return res


async def check_password(email, password):
    query = "SELECT * FROM Users WHERE email= ? AND password=?;"
    res = await DB_access.execute_query(query, (email, password))
    if res:
        return res
    else:
        raise InvalidLoginError
