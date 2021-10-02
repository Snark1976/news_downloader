import requests
import time
from bs4 import BeautifulSoup
from collections import namedtuple

News = namedtuple('News', 'date source title description link media tags')


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/94.0.4606.61 '
                         'Safari/537.36'}


def parser_lenta_ru():
    page = requests.get('https://lenta.ru/rss/', headers=headers)
    result = []
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'xml')        # Use 'xml' for RSS-channel OR 'lxml' for page of site
        all_news_this_source = soup.find_all('item')
        for news_this_source in all_news_this_source:
            news = News(date=time.mktime(time.strptime(news_this_source.pubDate.text[:-6], "%a, %d %b %Y %H:%M:%S")),
                        source='lenta.ru',
                        title=news_this_source.title.text,
                        description=news_this_source.description.text.strip(),
                        link=news_this_source.link.text,
                        media=str(news_this_source.find('enclosure')).split('"')[5],
                        tags=None
                        )
            result.append(news)
    else:
        result.append(f'Status: {page.status_code}')    # Change for logging
    return result


all_news = []
dict_parsers = {'https://lenta.ru/rss/': parser_lenta_ru}

for parser in dict_parsers.values():
    all_news.extend(parser())

print(*sorted(all_news), sep='\n')
