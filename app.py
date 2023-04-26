from icalendar import Calendar
from datetime import datetime, timedelta
from moodleAPI import MoodleAPI
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


def moodle_schedule_notify():
    print(f'現在時間：{datetime.now()}')
    line_notification_token = config.get(
        'notification_token', 'line_token')

    print(f'開始檢查課程事件...')
    
    courses = moodle_api.get_courses()
    for course in courses:
        schedule = moodle_api.get_course_schedule(course['url'])
        new_post_str = [
            f"標題：{ele['title']}\n發布時間：\n{ele['datetime']}\n教師：{ele['teacher']}" for ele in schedule['new_post']]
        new_post_str = f"\n------------------------------\n".join(new_post_str)
       
        notify_str = f"近期課程公告\n------------------------------\n{course['name'].center(38)}\n------------------------------\n{new_post_str}"
        if schedule['new_post']:
            print(f"{notify_str}")
            lineNotifyMessage(line_notification_token, notify_str)

        future_schedule_str = [
            f"標題：{ele['title']}\n開始時間：\n{ele['start']}\n結束時間：\n{ele['end']}\n教師：{ele['teacher']}" for ele in schedule['future_schedule']]
        future_schedule_str = f"\n------------------------------\n".join(future_schedule_str)
        notify_str = f"未來事件\n------------------------------\n{course['name'].center(38)}\n------------------------------\n{future_schedule_str}"
        if schedule['future_schedule']:
            print(f"{notify_str}")
            lineNotifyMessage(line_notification_token, notify_str)
        
    print('檢查結束\n---------------------------')


if __name__ == '__main__':
    try:
        moodle_api = MoodleAPI(config.get('moodle', 'username'),config.get('moodle', 'password'))
        moodle_schedule_notify()
        schedule.every().day.at("09:00").do(moodle_schedule_notify)
        while True:
            schedule.run_pending()
            time.sleep(30)

    except Exception as e:
        logging.exception(e)
        print(e)
        input()
        
        
