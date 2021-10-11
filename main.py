from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, DateTime, ForeignKey, \
    Text, insert, select, func
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import logging
import parsers

metadata = MetaData()

engine = create_engine("mysql+pymysql://root:Colobuc@localhost/db_news")

db_news = engine.connect()

logging.basicConfig(filename="timeline.log", level=logging.INFO)

sources = Table('sources', metadata,
                Column('id', Integer(), primary_key=True),
                Column('name', String(100), nullable=False),
                Column('url', String(100),  unique=True),
                Column('logo', Text, nullable=False)
                )

source_urls = Table('source_urls', metadata,
                    Column('id', Integer(), primary_key=True),
                    Column('source_id', Integer(), ForeignKey('sources.id')),
                    Column('url', Text, nullable=False)
                    )

news = Table('news', metadata,
             Column('id', Integer(), primary_key=True),
             Column('source_id', Integer(), ForeignKey('sources.id')),
             Column('title', Text, nullable=False),
             Column('description', Text, nullable=False),
             Column('datetime', DateTime(), nullable=False),
             Column('link', String(768), unique=True),
             Column('media', Text),
             Column('tags', Text, nullable=False)
             )


# Compare the list of resources in the database (tables "sources" and "source_urls") and in the parser module
# (parsers.py). Add new resources to the database.
def check_resource_list():
    list_url_sources = [i[0] for i in db_news.execute(select([sources.c.url])).fetchall()]
    for resource in parsers.list_sources:
        try:
            if resource['url'] not in list_url_sources:
                db_news.execute(insert(sources),
                                name=resource['name'],
                                url=resource['url'],
                                logo=resource['logo'])

                for link in resource['links_of_parse']:
                    db_news.execute(insert(source_urls),
                                    source_id=get_source_id(resource['url']),
                                    url=link)
        except SQLAlchemyError:
            logging.exception(f'Error adding source to database: {resource}')


# Getting id from table "sources" by url value
def get_source_id(url):
    try:
        sel = select([sources]).where(sources.c.url == url)
        source_id = db_news.execute(sel).scalar()
        return source_id

    except SQLAlchemyError:
        logging.exception(f'Error getting the source ID. Link: {url}')


# Loading a list of fresh news from a source
def download_news(data_source):
    result = []
    func_parser = data_source['func_parser']
    func_checking_news = data_source['func_checking']
    urls_source = data_source['links_of_parse']

    list_news = func_parser(*urls_source)
    if source_id := get_source_id(data_source['url']):
        for news_ in list_news:
            if is_fresh_news(news_):
                news_['source_id'] = source_id
                result.append(func_checking_news(news_))
    return result


# Checking the presence of this news in the database
def is_fresh_news(this_news):
    try:
        sel = select([news.c.link]).where(news.c.link == this_news['link'])
        result = db_news.execute(sel).scalar()
        return not result

    except SQLAlchemyError:
        logging.exception(f'Error checking the presence of this news in the database: {this_news["link"]}')
        return False


def add_news_to_database(n_list):
    for news_ in n_list:
        try:
            db_news.execute(insert(news), news_)
        except SQLAlchemyError:
            logging.exception(f'Error adding news to database: {news_}')


def get_count_news():
    sel = select([func.count()]).select_from(news)
    result = db_news.execute(sel).scalar()
    return result


if __name__ == "__main__":
    metadata.create_all(engine)
    logging.info(f' Time: {datetime.now()}. Start loading news.')
    check_resource_list()
    count_news = get_count_news()
    news_list = []
    for source in parsers.list_sources:
        news_list.extend(download_news(source))
    news_list.sort(key=lambda x: x['datetime'])
    add_news_to_database(news_list)
    logging.info(f' Time: {datetime.now()}. Stop loading news. Added news to DB: {get_count_news() - count_news}')
