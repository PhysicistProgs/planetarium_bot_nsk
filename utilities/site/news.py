import re
import requests
from bs4 import BeautifulSoup
import markdownify
import pickle
import os.path


PLANETARIUM_SITE_PREFIX = 'https://www.nebo-nsk.ru'
CACHE_FILE_NAME = 'news.cache'


class News:
    def __init__(self, text, date, url):
        self.text = self._fix_text(text)
        self.date = date
        self.url = url

    def _fix_text(self, text):
        text = text.strip()
        text = text.replace("\n\n", "\n")
        return text

    def get_text(self):
        news_text = f'{self.text}\n\n[Новость на сайте]({self.url})'
        return news_text


def _get_news_urls():
    r = requests.get(f'{PLANETARIUM_SITE_PREFIX}/newslist')
    soup = BeautifulSoup(r.content, 'html.parser')
    titlenews_all = soup.find_all(class_='titlenews')
    hrefs = [titlenews.find('a').get('href') for titlenews in titlenews_all]
    news_hrefs = [f'{PLANETARIUM_SITE_PREFIX}{href}' for href in hrefs]

    return news_hrefs


def _parse_news():
    news_urls = _get_news_urls()
    news_all = []
    for news_url in news_urls[:3]:
        try:
            r = requests.get(f'{news_url}')
            soup = BeautifulSoup(r.content, 'html.parser')
            news_body = str(soup.find(class_='bodynews').find('div'))
            news_text = markdownify.markdownify(news_body, heading_style="ATX")
            news_date = soup.find(class_='datanews2').text.strip()
        except Exception:
            print(f"Can't parse news {news_url}")
        else:
            news = News(news_text, news_date, news_url)
            news_all.append(news)
    return news_all


def cache_news():
    news_all = _parse_news()
    with open(CACHE_FILE_NAME, 'wb') as file:
        pickle.dump(news_all, file)


def cache_file_is_exists():
    if os.path.isfile(CACHE_FILE_NAME):
        return True
    return False


def get_news_from_cache(number_news=3):
    if not cache_file_is_exists():
        cache_news()
    news_all = []
    try:
        with open(CACHE_FILE_NAME, 'rb') as file:
            news_all = pickle.load(file)
    except Exception as e:
        print(f'ERRR: {e}')
    else:
        news_all = news_all[:number_news]
    return news_all[::-1]
