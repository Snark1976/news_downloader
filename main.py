from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, DateTime, ForeignKey, \
    Text, insert, select
from sqlalchemy.exc import SQLAlchemyError
from requests.exceptions import RequestException
from datetime import datetime
import parsers

metadata = MetaData()

engine = create_engine("mysql+pymysql://root:Colobuc@localhost/db_news", echo=True)

db_news = engine.connect()

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
             Column('description', Text),
             Column('datetime', DateTime(), default=datetime.now),
             Column('link', String(768), unique=True),
             Column('media', Text),
             Column('tags', Text)
             )


# Compare the list of resources in the database (tables "sources" and "source_urls") and in the parser module
# (parsers.py). Add new resources to the database.
def check_resource_list():
    list_url_sources = [i[0] for i in db_news.execute(select([sources.c.url])).fetchall()]

    for resource in parsers.list_sources:
        if resource['url'] not in list_url_sources:
            db_news.execute(insert(sources),
                            name=resource['name'],
                            url=resource['url'],
                            logo=resource['logo'])

            for link in resource['links_of_parse']:
                db_news.execute(insert(source_urls),
                                source_id=get_source_id(resource['url']),
                                url=link)


def get_source_id(url):
    sel = select([sources]).where(sources.c.url == url)
    source_id = db_news.execute(sel).scalar()
    return source_id


def download_news(data_source):
    func_parser = data_source['func_parser']
    urls_source = data_source['links_of_parse']
    try:
        news_source = func_parser(*urls_source)
    except RequestException:
        news_source = []
    return news_source


def is_fresh_news(this_news):
    sel = select([news.c.link]).where(news.c.link == this_news['link'])
    result = db_news.execute(sel).scalar()
    print(result)
    return not result


def add_news_to_database(n_list, source_id):
    n = 0
    try:
        for news_ in n_list:
            if is_fresh_news(news_):
                news_['source_id'] = source_id
                db_news.execute(insert(news), news_)
                n += 1
    except SQLAlchemyError:
        pass
    return n


metadata.create_all(engine)

if __name__ == "__main__":
    check_resource_list()
    fresh_news = 0
    for source in parsers.list_sources:
        news_list = download_news(source)
        fresh_news += add_news_to_database(news_list,
                                           get_source_id(source['url']))
    print('Add news to DB: ', fresh_news)


