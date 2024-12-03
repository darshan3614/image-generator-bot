import os
import schedule
import time as tm
from datetime import time, timedelta, datetime

def job():
    os.system("python main.py")
   

schedule.every().minute.at(":01").do(job)

while True:
    schedule.run_pending()
    tm.sleep(1)
