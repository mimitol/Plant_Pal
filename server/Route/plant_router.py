from fastapi import APIRouter, Response, HTTPException, File, UploadFile
from DB.DB_patterns import Plant
from Logic.CRUD import plant_crud
from Logic.functionallity import prediction
from Logic.functionallity import image_functionallity
from typing import List
from exceptions import exceptions_handler


router = APIRouter()


# קבלת כל הצמחים
@router.get('/plantpal/plants')
async def get_all_plants():
    try:
        plants = await plant_crud.get_all_plants()
        return plants
    except Exception as ex:
        return exceptions_handler(ex)


# קבלת צמח לפי שם
@router.get('/plantpal/plant/{plant_name}')
async def get_plant(plant_name: str):
    try:
        plant = await plant_crud.get_plant(plant_name)
        return plant
    except Exception as ex:
        return exceptions_handler(ex)


# הוספת צמח
@router.post('/plantpal/plant')
async def add_plant(plant: Plant):
    try:
        res = await plant_crud.add_plant(plant)
        return res
    except Exception as ex:
        return exceptions_handler(ex)


# עדכון פרטי צמח
@router.put('/plantpal/plant/{plant_name}')
async def update_plant(plant_name: str, plant_data: Plant):
    try:
        updated_plant = await plant_crud.update_plant(plant_name, plant_data)
        return updated_plant
    except Exception as ex:
        return exceptions_handler(ex)


# מחיקת צמח
@router.delete('/plantpal/plant/{plant_name}')
async def delete_plant(plant_name):
    try:
        res = await plant_crud.delete_plant(plant_name)
        return res
    except Exception as ex:
        return exceptions_handler(ex)


#קבלת הפרדיקציה על הצמח
@router.post("/plantpal/plant/identify")
async def get_plant_categories(images: list[UploadFile] = File(...)):
    try:
        file_locations=await image_functionallity.save_images_in_temp_directory(images)
        # הפעלת פונקציית הזיהוי עם הנתיבים של הקבצים השמורים
        categories = await prediction.predictionFunc(file_locations)
        res = {"categories": categories, "uploaded_photos": file_locations}
        return res
    except Exception as ex:
        return exceptions_handler(ex)

#הוספת התמונות שהמשתמש שלח לפרדיקציה לתיקית הצמח
@router.put('/plantpal/plant/images/{selectedCategory}')
async def update_images_location(selectedCategory: int,uploaded_photos: List[str]):
    try:
        updated_img_location = await plant_crud.update_plant_images_folder(uploaded_photos,selectedCategory)
        return updated_img_location
    except Exception as ex:
        return exceptions_handler(ex)


