import requests
import maya
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from requests.exceptions import RequestException
import logging

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/94.0.4606.61 '
                         'Safari/537.36'}

logging.basicConfig(filename="timeline.log", level=logging.INFO)


def get_page(url):
    try:
        page = requests.get(url, headers=headers)

        if page.status_code == 200:
            return page
        else:
            logging.error(f'Page loading error. Status code: {page.status_code}, link: {url}.')

    except RequestException:
        logging.exception(f'Page loading error. Link: {url}')


def parser_n_plus_1(url):
    result = []

    if page := get_page(url):
        soup = BeautifulSoup(page.text, 'xml')
        all_news_this_source = soup.find_all('item')

        for news_this_source in all_news_this_source:
            try:
                news = {'datetime': maya.parse(news_this_source.pubDate.text).datetime(),
                        'title': news_this_source.title.text.replace('\xa0', ' '),
                        'description': None,
                        'link': news_this_source.link.text,
                        'media': str(news_this_source.find('media:content')).split('"')[3],
                        'tags': None
                        }
                result.append(news)

            except (LookupError, TypeError, AttributeError, NameError, ValueError):
                logging.exception(f'Parsing error. Parsed text: \n{news_this_source}')

    return result


def parser_dev_by(url):
    result = []

    if page := get_page(url):
        soup = BeautifulSoup(page.text, 'xml')
        all_news_this_source = soup.find_all('item')

        for news_this_source in all_news_this_source:
            try:
                news = {'datetime': maya.parse(news_this_source.pubDate.text).datetime(),
                        'title': news_this_source.title.text.replace('\xa0', ' '),
                        'description': news_this_source.description.text.strip().replace('\xa0', ' '),
                        'link': news_this_source.link.text,
                        'media': str(news_this_source.find('enclosure')).split('"')[3],
                        'tags': None
                        }
                result.append(news)

            except (LookupError, TypeError, AttributeError, NameError, ValueError):
                logging.exception(f'Parsing error. Parsed text: \n{news_this_source}')

    return result


def parser_bbc_russian(url):
    result = []

    if page := get_page(url):
        soup = BeautifulSoup(page.text, 'xml')
        all_news_this_source = soup.find_all('item')

        for news_this_source in all_news_this_source:
            try:
                news = {'datetime': maya.parse(news_this_source.pubDate.text).datetime(),
                        'title': news_this_source.title.text.replace('\xa0', ' '),
                        'description': news_this_source.description.text.strip().replace('\xa0', ' '),
                        'link': news_this_source.link.text,
                        'media': None,
                        'tags': None
                        }
                result.append(news)

            except (LookupError, TypeError, AttributeError, NameError, ValueError):
                logging.exception(f'Parsing error. Parsed text: \n{news_this_source}')

    return result


def parser_deutsche_welle(url):
    result = []

    if page := get_page(url):
        soup = BeautifulSoup(page.text, 'xml')
        all_news_this_source = soup.find_all('item')

        for news_this_source in all_news_this_source:
            try:
                news = {'datetime': maya.parse(news_this_source.pubDate.text).datetime(),
                        'link': news_this_source.link.text,
                        'title': news_this_source.title.text.replace('\xa0', ' '),
                        'description': news_this_source.description.text.strip().replace('\xa0', ' '),
                        'media': None,
                        'tags': None
                        }
                result.append(news)

            except (LookupError, TypeError, AttributeError, NameError, ValueError):
                logging.exception(f'Parsing error. Parsed text: \n{news_this_source}')

    return result


def parser_lenta_ru(url):
    result = []

    if page := get_page(url):
        soup = BeautifulSoup(page.text, 'xml')
        all_news_this_source = soup.find_all('item')

        for news_this_source in all_news_this_source:
            try:
                news = {'datetime': maya.parse(news_this_source.pubDate.text).datetime(),
                        'title': news_this_source.title.text.replace('\xa0', ' '),
                        'description': news_this_source.description.text.strip().replace('\xa0', ' '),
                        'link': news_this_source.link.text,
                        'media': str(news_this_source.find('enclosure')).split('"')[5],
                        'tags': news_this_source.category.text
                        }
                result.append(news)

            except (LookupError, TypeError, AttributeError, NameError, ValueError):
                logging.exception(f'Parsing error. Parsed text: \n{news_this_source}')

    return result


def parser_century22(*urls):
    result = []
    all_news_this_source = []

    for url in urls:
        if page := get_page(url):
            soup = BeautifulSoup(page.text, 'lxml')
            all_news_this_source.append(soup.find('article', class_='article-item article-item-3_4'))
            all_news_this_source.extend(soup.find_all('article', class_='article-item article-item-1_2'))

    for news_this_source in all_news_this_source:
        try:
            date = maya.parse(news_this_source.select('time')[0]['datatime']).datetime()
            date = datetime.utcnow() if datetime.now().date() == date.date() else date
            news = {'datetime': date.replace(second=0, microsecond=0, tzinfo=timezone.utc),
                    'title': news_this_source.select('h3.item_link a')[0].text.strip().replace('\xa0', ' '),
                    'description': None,
                    'link': news_this_source.select('h3.item_link a')[0]['href'],
                    'media': news_this_source.select('img')[0]['src'] if news_this_source.select('img') else None,
                    'tags': None
                    }
            result.append(news)

        except (LookupError, TypeError, AttributeError, NameError, ValueError):
            logging.exception(f'Parsing error. Parsed text: \n{news_this_source}')

    return result


def parser_n_plus_1_news_checking(news):

    if page := get_page(news['link']):
        try:
            soup = BeautifulSoup(page.text, 'lxml')
            tags = soup.find_all('a', attrs={'data-rubric': True})
            news['tags'] = ', '.join(tag.text for tag in tags)
            for paragraph in soup.select('div.body.js-mediator-article p'):
                if len(paragraph.text) > 100:
                    news['description'] = paragraph.text.strip().replace('\xa0', ' ').replace('\n', ' ')
                    break

        except (LookupError, TypeError, AttributeError, NameError, ValueError):
            logging.exception(f'Parsing error. Parsed page: \n{news["link"]}')

    return news


def parser_dev_by_news_checking(news):

    if page := get_page(news['link']):
        try:
            soup = BeautifulSoup(page.text, 'lxml')
            news['tags'] = [st.text
                            for st in soup.select('span.article-meta__item')
                            if 'Тег' in st.text
                            ][0].replace('Теги: ', '')

        except (LookupError, TypeError, AttributeError, NameError, ValueError):
            logging.exception(f'Parsing error. Parsed page: \n{news["link"]}')

    return news


def parser_bbc_russian_news_checking(news):

    if page := get_page(news['link']):
        try:
            soup = BeautifulSoup(page.text, 'lxml')
            meta_tags = soup.find_all('meta', attrs={'name': "article:tag"})
            news['tags'] = ', '.join(meta['content'] for meta in meta_tags)
            news['media'] = soup.select('div figure div img')[0]['src'] if soup.select('div figure div img') else None

        except (LookupError, TypeError, AttributeError, NameError, ValueError):
            logging.exception(f'Parsing error. Parsed page: \n{news["link"]}')

    return news


def parser_deutsche_welle_news_checking(news):

    if page := get_page(news['link']):
        try:
            soup = BeautifulSoup(page.text, 'lxml')
            tags = soup.select('div ul.smallList li')[2]
            news['tags'] = ''.join(tag.text for tag in tags if 'Темы' not in tag.text).strip()
            news['media'] = soup.select('div a img')[0]['src'] if soup.select('div a img') else None

        except (LookupError, TypeError, AttributeError, NameError, ValueError):
            logging.exception(f'Parsing error. Parsed page: \n{news["link"]}')

    return news


def parser_lenta_ru_news_checking(news):
    pass
    return news


def parser_century22_news_checking(news):

    if page := get_page(news['link']):
        try:
            soup = BeautifulSoup(page.text, 'lxml')
            tags = soup.select('div.content_column_footer div.page_tags a')
            news['tags'] = '. '.join(tag.text.strip() for tag in tags)
            news['description'] = soup.find('p', class_='text_strong').text.replace('\xa0', ' ')

        except (LookupError, TypeError, AttributeError, NameError, ValueError):
            logging.exception(f'Parsing error. Parsed page: \n{news["link"]}')

    return news


list_sources = [
    {'name': 'N+1: научные статьи, новости, открытия',
     'url': 'https://nplus1.ru',
     'logo': 'https://nplus1.ru/i/logo.png',
     'links_of_parse': ('https://nplus1.ru/rss', ),
     'func_parser': parser_n_plus_1,
     'func_checking': parser_n_plus_1_news_checking
     },
    {'name': 'ИТ в Беларуси | dev.by',
     'url': 'https://dev.by',
     'logo': 'https://dev.by/assets/logo-c39214c7aad5915941bcf4ccda40ac3641f2851d5ec7e897270da373ed9701ad.svg',
     'links_of_parse': ('https://dev.by/rss', ),
     'func_parser': parser_dev_by,
     'func_checking': parser_dev_by_news_checking
     },
    {'name': 'BBC News Русская служба',
     'url': 'https://www.bbc.com/russian',
     'logo': 'https://news.files.bbci.co.uk/ws/img/logos/og/russian.png',
     'links_of_parse': ('https://feeds.bbci.co.uk/russian/rss.xml', ),
     'func_parser': parser_bbc_russian,
     'func_checking': parser_bbc_russian_news_checking
     },
    {'name': 'Новости и аналитика о Германии, России, Европе, мире | DW',
     'url': 'https://www.dw.com/ru',
     'logo': 'https://www.dw.com/cssi/dwlogo-print.gif',
     'links_of_parse': ('https://rss.dw.com/xml/rss-ru-all', ),
     'func_parser': parser_deutsche_welle,
     'func_checking': parser_deutsche_welle_news_checking
     },
    {'name': 'Lenta.ru - Новости России и мира сегодня',
     'url': 'https://lenta.ru',
     'logo': 'https://lenta.ru/images/icons/icon-512x512.png',
     'links_of_parse': ('https://lenta.ru/rss/', ),
     'func_parser': parser_lenta_ru,
     'func_checking': parser_lenta_ru_news_checking
     },
    {'name': 'Новости науки, техники и технологий. 22 век',
     'url': 'https://22century.ru',
     'logo': 'https://22century.ru/wp-content/themes/xxiicentury_new/images/22_century_logo.png',
     'links_of_parse': ('https://22century.ru/news',
                        'https://22century.ru/popular-science-publications)'),
     'func_parser': parser_century22,
     'func_checking': parser_century22_news_checking
     },
]

if __name__ == "__main__":
    all_news = []
    for parser in list_sources:
        all_news.extend(parser['func_parser'](*parser['links_of_parse']))

    print(*sorted(all_news, key=lambda x: x['datetime'], reverse=True), len(all_news), sep='\n')
