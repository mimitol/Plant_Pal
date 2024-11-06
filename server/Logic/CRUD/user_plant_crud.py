from DB import DB_access
import pyodbc
from DB.DB_patterns import User_plant
from exceptions import InvalidInputError


async def get_all_user_plants():
    user_plants = await DB_access.execute_query("SELECT * FROM User_Plants")
    return user_plants


async def add_plant_to_user(user_plant: User_plant):
    user_exist = await DB_access.execute_query("SELECT * FROM Users WHERE user_id =?;", user_plant.user_id)
    plant_exist = await DB_access.execute_query("SELECT * FROM Plants WHERE plant_id =?;", user_plant.plant_id)
    if user_exist and plant_exist:
        new_user_plant = (
        user_plant.user_id, user_plant.plant_id, user_plant.date_added, user_plant.last_watering_reminder,
        user_plant.plant_status, user_plant.uploaded_photo)
        query = "INSERT INTO User_Plants (user_id,plant_id, date_added, last_watering_reminder,plant_status,uploaded_photo) VALUES (?, ?, ?, ?,?,?);"
        res = await DB_access.execute_query(query, new_user_plant)
        return res
    else:
        raise InvalidInputError


async def delete_users_plant(user_plant_id):
    query = "UPDATE User_Plants SET plant_status=0 WHERE id = ?;"
    res = await DB_access.execute_query(query, user_plant_id)
    return res


async def get_all_plants_of_user(user_id):
    query = """SELECT Plants.plant_name, User_Plants.uploaded_photo,id
    FROM Plants
    JOIN User_Plants ON Plants.plant_id = User_Plants.plant_id
    WHERE User_Plants.user_id = ? AND plant_status=1 ;"""
    plants = await DB_access.execute_query(query, user_id)
    return plants


async def update_user_plant(user_plant_id, user_plant: User_plant):
    updated_user_plant = (
        user_plant.last_watering_reminder, user_plant.plant_status, user_plant.uploaded_photo, user_plant_id)
    query = "UPDATE User_Plants SET last_watering_reminder=? plant_status=?, uploaded_photo=? id = ?;"
    res = await DB_access.execute_query(query, updated_user_plant)
    return res


async def get_plant_of_user(user_plant_id):
    query = """SELECT *
    FROM Plants
    JOIN User_Plants ON Plants.plant_id = User_Plants.plant_id
    WHERE User_Plants.id = ?;"""
    user_plant = await DB_access.execute_query(query,user_plant_id)
    return user_plant
