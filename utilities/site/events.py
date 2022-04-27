from asyncio import events
from bs4 import BeautifulSoup
import re
import requests
import pickle
import os.path


PLANETARIUM_SITE_PREFIX = 'https://www.nebo-nsk.ru'
CACHE_FILE_NAME = 'events.cache'


class Event:
    def __init__(self, title, description, date, url):
        self.title = self._fix_text(title)
        self.description = self._fix_text(description)
        self.date = date
        self.url = url

    def _fix_text(self, text):
        text = text.strip()
        text = text.replace("\n\n", "\n")
        text = text.replace('Подробнее', '')
        return text

    def get_text(self):
        return f'**{self.title}** {self.date}\n{self.description}\n\n[Подробнне]({self.url})'


def _is_technical_day(soup):
    contain_view_empty = soup.find(class_='view-empty')
    if contain_view_empty:
        return True
    return False


def _parse_events_from_url(source):
    events = []
    r = requests.get(f'{PLANETARIUM_SITE_PREFIX}/{source}')
    soup = BeautifulSoup(r.content, 'html.parser')
    if _is_technical_day(soup):
        technical_event = Event(
            'Извините, но на выбранную дату мероприятия не запланированы:(',
            'Понедельник - технический день!',
            '',
            'https://nebo-nsk.ru/my-calendar',
        )
        events.append(technical_event)
        return events
    event_views = soup.find(class_='view-content').find_all(class_=re.compile("^views-row"))
    for view in event_views:
        try:
            title = view.find(class_='zagcal').text
            description = view.find(class_='opcal').text
            date = view.find(class_='date-display-single').text
            url_postfix = view.find(class_='zagcal').find('a').get('href')
            url = f"{PLANETARIUM_SITE_PREFIX}{url_postfix}"
        except Exception:
            print(f"Can't parse news {url}")
        else:
            event = Event(title, description, date, url)
            events.append(event)
    return events


def _parse_events():
    today_events = _parse_events_from_url('my-calendar-today')
    tomorrow_events = _parse_events_from_url('my-calendar-tomorrow')
    events = {'today': today_events, 'tomorrow': tomorrow_events}
    return events


def cache_events():
    events = _parse_events()
    with open(CACHE_FILE_NAME, 'wb') as file:
        pickle.dump(events, file)


def cache_file_is_exists():
    if os.path.isfile(CACHE_FILE_NAME):
        return True
    return False


def get_events_from_cache():
    if not cache_file_is_exists():
        cache_events()
    try:
        with open(CACHE_FILE_NAME, 'rb') as file:
            events = pickle.load(file)
    except Exception as e:
        print(f'ERRR: {e}')
    else:
        return events


def get_today_events_from_cache():
    events = get_events_from_cache()
    today_events = events['today']
    return today_events


def get_tomorrow_events_from_cache():
    events = get_events_from_cache()
    tomorrow_events = events['tomorrow']
    return tomorrow_events
