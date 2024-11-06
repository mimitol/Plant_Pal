from fastapi import APIRouter,Response
from DB.DB_patterns import User_plant
from Logic.CRUD import user_plant_crud
from exceptions import exceptions_handler

router = APIRouter()


@router.get('/plantpal/user/plants/{user_id}')
async def get_all_plants_of_user(user_id):
    try:
        plants_of_user = await user_plant_crud.get_all_plants_of_user(user_id)
        return plants_of_user
    except Exception as ex:
        return exceptions_handler(ex)


@router.get('/plantpal/user/plant/{user_plant_id}')
async def get_plant_of_user(user_plant_id):
    try:
        plant_of_user = await user_plant_crud.get_plant_of_user(user_plant_id)
        return plant_of_user
    except Exception as ex:
        return exceptions_handler(ex)

@router.post('/plantpal/user/plant')
async def add_plant_to_user(plant:User_plant):
    try:
        result = await user_plant_crud.add_plant_to_user(plant)
        return result
    except Exception as ex:
        return exceptions_handler(ex)

@router.delete('/plantpal/user/plant/{user_plant_id}')
async def delete_users_plant(user_plant_id):
    try:
        result = await user_plant_crud.delete_users_plant(user_plant_id)
        return result
    except Exception as ex:
        return exceptions_handler(ex)



@router.put('/plantpal/user/plant/{user_plant_id}')
async def update_users_plant(user_plant_id, users_plant_data: User_plant):
    try:
        updated_users_plant = await user_plant_crud.update_user_plant(user_plant_id, users_plant_data)
        return updated_users_plant
    except Exception as ex:
        return exceptions_handler(ex)




