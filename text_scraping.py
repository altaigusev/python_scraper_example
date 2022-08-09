import requests
from requests_html import HTMLSession
from tz_scraper import text_grabber, text_saver


session = HTMLSession()
url_file = open('url_list.txt', 'r')
url_list = url_file.read().splitlines()
for url in url_list:
    print(url)
    try:
        grabbed_text = text_grabber(session, url)
        grabbed_text = grabbed_text + '-'*50 + '\n' + f'{url}' + '\n'
    except requests.exceptions.SSLError:
        print('Сертификат сайта просрочен или его блокирует провайдер')
        grabbed_text = f'{url} - Сертификат сайта просрочен или его блокирует провайдер\n' + '-'*50 + '\n'
        continue
    try:
        text_saver(grabbed_text)
    except UnicodeEncodeError:
        print(f'Идиотский сайт: {url}')
        continue
