from fastapi import FastAPI, APIRouter
import uvicorn
from Route import user_router,plant_router,users_plant__router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from Logic.functionallity.reminder import watering_reminder
from fastapi import FastAPI, BackgroundTasks
from multiprocessing import Process
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import schedule
import time
import asyncio
app = FastAPI()
router = APIRouter()
app.mount("/images", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "images")), name="images")

# הוסף middleware ל-CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # לשים לב להגביל זאת למקורות מסוימים בסביבה האמיתית
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
@router.get("/")
async def simple_get():
    return "hi"

# Include the router with the route in your app
app.include_router(router)
app.include_router(user_router.router)
app.include_router(plant_router.router)
app.include_router(users_plant__router.router)

scheduler = AsyncIOScheduler()
# הגדרת משימה שמופעלת שלוש פעמים ביום
def schedule_task():
    scheduler.add_job(watering_reminder, CronTrigger(hour=12, minute=22),args=['morning'])
    scheduler.add_job(watering_reminder, CronTrigger(hour=16, minute=0), args=['afternoon'])
    scheduler.add_job(watering_reminder, CronTrigger(hour=19, minute=0), args=['evening'])
    scheduler.start()

# יצירת פונקציה שתוקדש להתחלת השרת
@app.on_event("startup")
async def startup_event():
    schedule_task()

# הרצת השרת ב-UVICORN
def run_server():
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

# יצירת תהליך להרצת השרת
server_process = Process(target=run_server)

if __name__ == '__main__':
    # התחלת התהליכים
    server_process.start()
    try:
        # שמירת התזמון פועל ברקע
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
