import os
from datetime import datetime
from fastapi import APIRouter, Response, HTTPException, File, UploadFile

async def save_images_in_temp_directory(images: list[UploadFile] = File(...)):
    file_locations = []
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")[:-3]
    i = 1
    for file in images:
        file_extension = os.path.splitext(file.filename)[1]
        new_filename = f"{timestamp}{i}{file_extension}"
        i += 1
        # שמירת הקובץ בתיקייה uploads עם השם החדש
        file_location = os.path.join(upload_dir, new_filename)
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # הוספת המיקום של הקובץ החדש לרשימה של מיקומי הקבצים
        file_locations.append(file_location)
    return file_locations