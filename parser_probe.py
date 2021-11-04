# import requests
# import maya
# from bs4 import BeautifulSoup
# from collections import namedtuple
# from requests.exceptions import RequestException
# import logging
#
# News = namedtuple('News', 'date source title description link media tags')
#
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
#                          'AppleWebKit/537.36 (KHTML, like Gecko) '
#                          'Chrome/94.0.4606.61 '
#                          'Safari/537.36'}
#
# logging.basicConfig(filename="news_downloader.log", level=logging.INFO)
#
#
# def get_page(url):
#     page = requests.get(url, headers=headers)
#     if page.status_code == 200:
#         return page
#     else:
#         logging.error(f'Page loading error. Status code: {page.status_code}, link: {url}.')
#
#
# def parser_n_plus_1(url):
#     result = []
#     if page := get_page(url):
#         soup = BeautifulSoup(page.text, 'xml')
#         all_news_this_source = soup.find_all('item')
#
#         for news_this_source in all_news_this_source:
#             news = {'datetime': maya.parse(news_this_source.pubDate.text).datetime(),
#                     'title': news_this_source.title.text.replace('\xa0', ' '),
#                     'description': None,
#                     'link': news_this_source.link.text,
#                     'media': str(news_this_source.find('media:content')).split('"')[3],
#                     'tags': None
#                     }
#             result.append(news)
#
#     return result
#
#
# def parser_n_plus_1_news_checking(news):
#     page = requests.get(news['link'], headers=headers)
#
#     if page.status_code == 200:
#         soup = BeautifulSoup(page.text, 'lxml')
#         tags = soup.find_all('a', attrs={'data-rubric': True})
#         news['tags'] = ', '.join(tag.text for tag in tags)
#         for paragraph in soup.select('div.body.js-mediator-article p'):
#             if len(paragraph.text) > 100:
#                 news['description'] = paragraph.text.strip().replace('\xa0', ' ').replace('\n', ' ')
#                 break
#     else:
#         logging.error(f'Status code: {page.status_code}, link: {news["link"]}, function: {__name__}')
#     return news
#
#
# list_parsers = [
#     {'name': 'N+1: научные статьи, новости, открытия',
#      'url': 'https://nplus1.ru',
#      'logo': 'https://nplus1.ru/i/logo.png',
#      'links_of_parse': ('https://nplus1.ru/ rss', ),
#      'func_parser': parser_n_plus_1,
#      'func_checking': parser_n_plus_1_news_checking
#      },
# ]
#
# if __name__ == "__main__":
#     all_news = []
#     try:
#         for parser in list_parsers:
#             all_news.extend(parser['func_parser'](*parser['links_of_parse']))
#     except RequestException:
#         pass
#     print(*sorted(all_news, key=lambda x: x['datetime'], reverse=True), len(all_news), sep='\n')
