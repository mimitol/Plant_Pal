from DB import DB_access
from DB.DB_patterns import Plant
import shutil
from urllib.parse import urlparse
from pathlib import Path
from exceptions import DBConnectionError, QueryExecutionError, InvalidSignupError, InvalidLoginError,InvalidInputError,AlreadyExistError

async def get_all_plants():
    plants = await DB_access.execute_query("SELECT * FROM Plants")
    return plants


async def add_plant(plant: Plant):
    exist = await DB_access.execute_query("SELECT * FROM Plants WHERE plant_name =?;", plant.plant_name)
    if not exist:
        new_plant = (
        plant.plant_name, plant.picture, plant.watering_frequency, plant.picture_folder_path, plant.general_info,
        plant.treatment, plant.id_in_model)
        query = "INSERT INTO Plants (plant_name,picture,watering_frequency, picture_folder_path, general_info,treatment,id_in_model) VALUES (?, ?, ?, ?,?,?,?);"
        res = await DB_access.execute_query(query, new_plant)
        return res
    else:
        raise AlreadyExistError


async def delete_plant(plant_name):
    query = "DELETE FROM Plants WHERE plant_name= ?;"
    res = await DB_access.execute_query(query, plant_name)
    return res


async def get_plant(plant_name):
    query = "SELECT * FROM Plants WHERE plant_name= ?;"
    res = await DB_access.execute_query(query, plant_name)
    return res


async def update_plant(plant_name, plant: Plant):
    print(plant.picture)
    updated_plant = (
    plant.id_in_model, plant.picture, plant.watering_frequency, plant.picture_folder_path, plant.general_info,
    plant.treatment, plant_name)
    query = "UPDATE Plants SET id_in_model=?, picture=?, watering_frequency=?, picture_folder_path=?, general_info = ?,treatment=? WHERE plant_name = ?;"
    res = await DB_access.execute_query(query, updated_plant)
    return res


async def update_plant_images_folder(uploaded_images, selected_category):
    try:
        # נתיב לתיקיית היעד
        res = await DB_access.execute_query('SELECT picture_folder_path FROM Plants WHERE id_in_model=?', selected_category)
        destination_folder = res[0].get('picture_folder_path')
        print(destination_folder)
        for image_location in uploaded_images:
            source_path = image_location
            shutil.copy(source_path, destination_folder)
        uploaded_image_name=uploaded_images[0]
        uploaded_image_name=uploaded_image_name.split("\\")[-1]
        return f"http://127.0.0.1:8000/images/{selected_category}/{uploaded_image_name}"
    except Exception:
        raise InvalidInputError

