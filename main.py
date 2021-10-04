from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, DateTime, ForeignKey, \
    Text, insert, select
from sqlalchemy.exc import IntegrityError
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

    for pars in parsers.list_sources:
        if pars['url'] not in list_url_sources:
            db_news.execute(insert(sources),
                            name=pars['name'],
                            url=pars['url'],
                            logo=pars['logo'])

            s = select([sources]).where(sources.c.url == pars['url'])
            source_id = db_news.execute(s).scalar()

            for link in pars['links_of_parse']:
                db_news.execute(insert(source_urls),
                                source_id=source_id,
                                url=link)


def processing_news(data_source):
    func_parser = data_source['func_parser']
    urls_source = data_source['links_of_parse']
    news_source = func_parser(*urls_source)

    try:
        db_news.execute(insert(news), news_source)
    except IntegrityError:
        pass


metadata.create_all(engine)

if __name__ == "__main__":
    check_resource_list()
    for source in parsers.list_sources:
        processing_news(source)

