### loading the NM utils
from .notifyme_utils import scan_new_register, scan_waiting_list
import schedule
import time

schedule.every(2).hours.do(scan_new_register)
schedule.every().day.at("02:00").do(scan_waiting_list)

while True:
       schedule.run_pending()
       time.sleep(1)
