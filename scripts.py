import schedule
import time
from app.service.hp_face_recognition import job


schedule.every().hours.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)