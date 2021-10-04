import requests
import maya
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/94.0.4606.61 '
                         'Safari/537.36'}


def parser_n_plus_1(url):
    result = []
    page = requests.get(url, headers=headers)

    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'xml')
        all_news_this_source = soup.find_all('item')

        for news_this_source in all_news_this_source:
            news = {'datetime': maya.parse(news_this_source.pubDate.text).datetime(),
                    'title': news_this_source.title.text,
                    'description': news_this_source.description.text.strip(),
                    'link': news_this_source.link.text,
                    'media': str(news_this_source.find('media:content')).split('"')[3],
                    'tags': None
                    }
            result.append(news)

        return result


def parser_dev_by(url):
    result = []
    page = requests.get(url, headers=headers)

    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'xml')
        all_news_this_source = soup.find_all('item')

        for news_this_source in all_news_this_source:
            news = {'datetime': maya.parse(news_this_source.pubDate.text).datetime(),
                    'title': news_this_source.title.text,
                    'description': news_this_source.description.text.strip().replace('\xa0', ' '),
                    'link': news_this_source.link.text,
                    'media': str(news_this_source.find('enclosure')).split('"')[3],
                    'tags': None
                    }
            result.append(news)

        return result


def parser_bbc_russian(url):
    result = []
    page = requests.get(url, headers=headers)

    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'xml')
        all_news_this_source = soup.find_all('item')

        for news_this_source in all_news_this_source:
            news = {'datetime': maya.parse(news_this_source.pubDate.text).datetime(),
                    'title': news_this_source.title.text,
                    'description': news_this_source.description.text.strip(),
                    'link': news_this_source.link.text,
                    'media': None,
                    'tags':None
                    }
            result.append(news)

        return result


def parser_deutsche_welle(url):
    result = []
    page = requests.get(url, headers=headers)

    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'xml')
        all_news_this_source = soup.find_all('item')

        for news_this_source in all_news_this_source:
            news = {'datetime': maya.parse(news_this_source.pubDate.text).datetime(),
                    'title': news_this_source.title.text,
                    'description': news_this_source.description.text.strip(),
                    'link': news_this_source.link.text,
                    'media': None,
                    'tags': None
                    }
            result.append(news)

        return result


def parser_lenta_ru(url):
    result = []
    page = requests.get(url, headers=headers)

    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'xml')
        all_news_this_source = soup.find_all('item')

        for news_this_source in all_news_this_source:
            news = {'datetime': maya.parse(news_this_source.pubDate.text).datetime(),
                    'title': news_this_source.title.text,
                    'description': news_this_source.description.text.strip(),
                    'link': news_this_source.link.text,
                    'media': str(news_this_source.find('enclosure')).split('"')[5],
                    'tags': None
                    }
            result.append(news)

        return result


def parser_century22(*url):
    result = []
    all_news_this_source = []

    page = requests.get(url[0], headers=headers)

    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'lxml')
        all_news_this_source.append(soup.find('article', class_='article-item article-item-3_4'))
        all_news_this_source.extend(soup.find_all('article', class_='article-item article-item-1_2'))

    page = requests.get(url[1], headers=headers)

    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'lxml')
        all_news_this_source.append(soup.find('article', class_='article-item article-item-3_4'))
        all_news_this_source.extend(soup.find_all('article', class_='article-item article-item-1_2'))

    for news_this_source in all_news_this_source:
        news = {'datetime': maya.parse(news_this_source.select('time')[0]['datatime']).datetime(),
                'title': news_this_source.select('h3.item_link a')[0].text.strip().replace('\xa0', ' '),
                'description': None,
                'link': news_this_source.select('h3.item_link a')[0]['href'],
                'media': news_this_source.select('img')[0]['src'],
                'tags': None
                }
        result.append(news)

    return result


list_sources = [{'name': 'N+1: научные статьи, новости, открытия',
                 'url': 'https://nplus1.ru',
                 'logo': 'https://nplus1.ru/i/logo.png',
                 'links_of_parse': ('https://nplus1.ru/rss', ),
                 'func_parser': parser_n_plus_1
                 },
                {'name': 'ИТ в Беларуси | dev.by',
                 'url': 'https://dev.by',
                 'logo': 'https://dev.by/assets/logo-c39214c7aad5915941bcf4ccda40ac3641f2851d5ec7e897270da373ed9701ad.svg',
                 'links_of_parse': ('https://dev.by/rss', ),
                 'func_parser': parser_dev_by
                 },
                {'name': 'BBC News Русская служба',
                 'url': 'https://www.bbc.com/russian',
                 'logo': 'https://news.files.bbci.co.uk/ws/img/logos/og/russian.png',
                 'links_of_parse': ('http://feeds.bbci.co.uk/russian/rss.xml', ),
                 'func_parser': parser_bbc_russian
                 },
                {'name': 'Новости и аналитика о Германии, России, Европе, мире | DW',
                 'url': 'https://www.dw.com/ru',
                 'logo': 'https://www.dw.com/cssi/dwlogo-print.gif',
                 'links_of_parse': ('https://rss.dw.com/xml/rss-ru-all', ),
                 'func_parser': parser_deutsche_welle
                 },
                {'name': 'Lenta.ru - Новости России и мира сегодня',
                 'url': 'https://lenta.ru',
                 'logo': 'https://lenta.ru/images/icons/icon-512x512.png',
                 'links_of_parse': ('https://lenta.ru/rss/', ),
                 'func_parser': parser_lenta_ru
                 },
                {'name': 'Новости науки, техники и технологий. 22 век',
                 'url': 'https://22century.ru',
                 'logo': 'https://22century.ru/wp-content/themes/xxiicentury_new/images/22_century_logo.png',
                 'links_of_parse': ('https://22century.ru/news',
                                    'https://22century.ru/popular-science-publications)'),
                 'func_parser': parser_century22
                 },
                ]

if __name__ == "__main__":
    all_news = []
    for parser in list_sources:
        all_news.extend(parser['func_parser'](*parser['links_of_parse']))

    print(*sorted(all_news, key=lambda x: x['datetime'], reverse=True), len(all_news), sep='\n')
