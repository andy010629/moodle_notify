import requests
from bs4 import BeautifulSoup



def moodle_login(username, password):
  rs = requests.Session()
  url = 'https://moodle.mcu.edu.tw/'
  headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
      'AppleWebKit/537.36 (KHTML, like Gecko) '
      'Chrome/89.0.4389.82 Safari/537.36'
  }

  response = rs.get(url, headers=headers)
  soup = BeautifulSoup(response.text, 'lxml')
  login_token = soup.select_one('[name=logintoken]')['value']
  login_url = 'https://moodle.mcu.edu.tw/login/index.php'
  login_data = {
      'username': username,
      'password': password,
      'logintoken': login_token
  }

  # 登入主站
  rs.post(login_url, headers=headers, data=login_data)

  return rs


def get_ics_response(rs, subsite='moodle3-06'):

  res = rs.get(f'https://{subsite}.mcu.edu.tw/login/index.php')
  soup = BeautifulSoup(res.text, 'lxml')
  redirect_site_url = (soup.select_one(
      '#region-main > div > div > div.signuppanel > div > div > div > a')['href'])
  res = rs.get(redirect_site_url)
  export_url = f'https://{subsite}.mcu.edu.tw/calendar/export.php'
  res = rs.get(export_url)
  soup = BeautifulSoup(res.text, 'lxml')
  sesskey = soup.select_one('[name=sesskey]')['value']
  export_data = {
      'sesskey': sesskey,
      '_qf__core_calendar_export_form': '1',
      'events[exportevents]': 'all',
      'period[timeperiod]': 'recentupcoming',
      'generateurl': 'Location'
  }
  res = rs.post(export_url, data=export_data)
  soup = BeautifulSoup(res.text, 'lxml')

  calendarurl = soup.select_one('.calendarurl').text.split(': ')[-1]
  res = rs.get(calendarurl)

  return res

