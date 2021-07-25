### loading the NM utils
import Notifyme_utils as ut
import schedule
import time

schedule.every(2).hours.do(ut.scan_new_register)
schedule.every().day.at("02:00").do(ut.scan_waiting_list)

while True:
       schedule.run_pending()
       time.sleep(1)