from icalendar import Calendar
from datetime import datetime, timedelta
from moodle_utils import moodle_login, get_ics_response
import sys
import os
import configparser
import os
import pytz
from notify import lineNotifyMessage
import schedule
import time
import logging


if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))



config_path = os.path.join(application_path, 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)


def moodle_calendar_notify():
  print(f'現在時間：{datetime.now()}')
  moodle_username = config.get('moodle', 'username')
  moodle_password = config.get('moodle', 'password')
  moodle_subsite = config.get('moodle', 'subsite')
  line_notification_token = config.get(
      'notification_token', 'line_token')

  print(f'開始檢查 {moodle_username} 行事曆...')

  session = moodle_login(moodle_username, moodle_password)
  response = get_ics_response(session, moodle_subsite)

  if response.status_code == 200:
      cal = Calendar.from_ical(response.text)

      for event in cal.walk('vevent'):
          tz = pytz.timezone('Asia/Taipei')
          summary = event.get('summary')
          dtstart = event.get('dtstart').dt.astimezone(tz)
          dtend = event.get('dtend').dt.astimezone(tz)
          now = datetime.now(tz)
          summary_str = f"{summary}\n----------------------------\n開始時間：\n{dtstart.strftime('%Y-%m-%d %H:%M:%S')}\n結束時間：\n{dtend.strftime('%Y-%m-%d %H:%M:%S')}"

          # if now-timedelta(days=3) > dtend:
          #     continue
          

          if now-timedelta(days=3) > dtstart or now < dtend+timedelta(days=3):
              print(f"事件：{summary}")
              print(f"開始時間：{dtstart}")
              print(f"結束時間：{dtend}")
              print()
              notify_str = f" 近期事件\n{summary_str}"
              lineNotifyMessage(line_notification_token, notify_str)
              continue

          if now < dtend + timedelta(days=3):
            print(f"事件：{summary}")
            print(f"開始時間：{dtstart}")
            print(f"結束時間：{dtend}")
            print()
            notify_str = f" 即將過期\n{summary_str}"
            lineNotifyMessage(line_notification_token, notify_str)
          
            
  else:
      print(f"無法下載ICS檔案：HTTP {response.status_code}")
  print('檢查結束\n---------------------------')


if __name__ == '__main__':
  try:
    moodle_calendar_notify()
    schedule.every().day.at("09:00").do(moodle_calendar_notify)
    while True:
      schedule.run_pending()
      time.sleep(30)
  except Exception as e:
    logging.exception(e)
    print(e)
    input()
    
    
