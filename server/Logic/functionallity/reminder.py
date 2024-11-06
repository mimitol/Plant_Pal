import sys
import os
from DB import DB_access

# הוספת התיקייה הנוכחית ל-PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ייבוא הפונקציה
from firebase_notifications import send_fcm_message


# קריאת הפונקציה
async def watering_reminder(time_in_day):
    users_to_remind = await DB_access.execute_query("""SELECT  p.plant_name, u.user_name, u.token_for_notifications
                                FROM users u
                                INNER JOIN
                                user_plants utp ON u.user_id = utp.user_id
                                INNER JOIN
                                plants p ON utp.plant_id = p.plant_id
                                WHERE
                                utp.plant_status = 1 AND
                                DATEDIFF(day, utp.last_watering_reminder, GETDATE())> p.watering_frequency AND
                                u.watering_hours =?""", time_in_day)
    print(users_to_remind)
    for user in users_to_remind:
        send_fcm_message(user.plant_name, user.token_for_remainders, user.user_name)

    await watering_reminder("morning")
