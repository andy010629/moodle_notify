import requests
from bs4 import BeautifulSoup
from datetime import datetime

class MoodleAPI:
    def __init__(self, username:str, password:str,baseurl='https://moodle.mcu.edu.tw/'):
        self.session = requests.Session()
        self.baseurl = baseurl
        self.__username = username
        self.__password = password
        self.moodle_login()

    def moodle_login(self) -> requests.Session:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/89.0.4389.82 Safari/537.36'
        }

        response = self.session.get(self.baseurl, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        login_token = soup.select_one('[name=logintoken]')['value']
        login_url = f'{self.baseurl}/login/index.php'
        login_data = {
            'username': self.__username,
            'password': self.__password,
            'logintoken': login_token
        }
        self.session.post(login_url, headers=headers, data=login_data)


    def get_courses(self) -> list:
        response = self.session.get(self.baseurl)
        soup = BeautifulSoup(response.text, 'lxml')
        course_soup = [ele.parent for ele in soup.select('[title=主機]')]
        courses = [
            {
                'course_id': ele.text[:11].split('-')[-1],
                'name': ele.text[11:],
                'url': ele['href']  
            } for ele in course_soup
        ]
        return courses
    
    def get_course_schedule(self,course_url:str) -> dict:
        response = self.session.get(course_url)
        soup = BeautifulSoup(response.text, 'lxml')
        new_post = [{
            'title': ele.select_one('a').text,
            'datetime': ele.select_one('.date').text,
            'teacher': ele.select_one('.name').text.replace(' ', ''),
        } for ele in soup.select('#inst38787 > div.content > ul > li')]

        # convert to datetime object
        for ele in new_post:
            ele['datetime'] = datetime.strptime(ele['datetime'], '%m月 %d日,%H:%M')
            ele['datetime'] = ele['datetime'].replace(year=datetime.now().year)

        future_schedule =[{
            'title': ele.select_one('a').text,
            'datetime': ele.select_one('.date').text,
            'teacher': ele.select_one('.name').text.replace(' ', ''),
        }
        for ele in soup.select('#inst38788 > div.content > ul > li')]
        for ele in future_schedule:
            ele['datetime'] = datetime.strptime(ele['datetime'], '%m月 %d日,%H:%M')
            ele['datetime'] = ele['datetime'].replace(year=datetime.now().year)
        
        return {'new_post': new_post, 'future_schedule': future_schedule}

    def get_ics_response(self, subsite='moodle3-06'):
        res = self.session.get(f'https://{subsite}.mcu.edu.tw/login/index.php')
        soup = BeautifulSoup(res.text, 'lxml')
        redirect_site_url = (soup.select_one(
            '#region-main > div > div > div.signuppanel > div > div > div > a')['href'])
        res = self.session.get(redirect_site_url)
        export_url = f'https://{subsite}.mcu.edu.tw/calendar/export.php'
        res = self.session.get(export_url)
        soup = BeautifulSoup(res.text, 'lxml')
        sesskey = soup.select_one('[name=sesskey]')['value']
        export_data = {
            'sesskey': sesskey,
            '_qf__core_calendar_export_form': '1',
            'events[exportevents]': 'all',
            'period[timeperiod]': 'recentupcoming',
            'generateurl': 'Location'
        }
        res = self.session.post(export_url, data=export_data)
        soup = BeautifulSoup(res.text, 'lxml')
        calendarurl = soup.select_one('.calendarurl').text.split(': ')[-1]
        res = self.session.get(calendarurl)
        return res


if __name__ == '__main__':
    username = '10363035'
    password = 'andy900629'
    moodle = moodleAPI(username, password)
    courses = moodle.get_courses()
    moodle.get_course_schedule(courses[0]['url'])