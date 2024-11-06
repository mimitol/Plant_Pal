from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    user_name: str
    email: str
    password: str
    watering_hours: str
    interested_in_reminders: bool
    token_for_reminders: str

class Plant(BaseModel):
    plant_name:str
    picture:str
    watering_frequency:float
    picture_folder_path:str
    general_info:str
    treatment:str
    id_in_model:int

class User_plant(BaseModel):
    user_id:int
    plant_id:int
    date_added: datetime
    last_watering_reminder:datetime
    plant_status:bool
    uploaded_photo:str
