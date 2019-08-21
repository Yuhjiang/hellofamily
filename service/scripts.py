import schedule
import time
from service.hp_face_recognition import job


schedule.every().minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
