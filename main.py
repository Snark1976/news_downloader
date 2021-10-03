from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, DateTime, ForeignKey, \
    Text, insert, select
from datetime import datetime
import parsers

metadata = MetaData()

engine = create_engine("mysql+pymysql://root:Colobuc@localhost/db_news", echo=True)

db_news = engine.connect()

sources = Table('sources', metadata,
                Column('id', Integer(), primary_key=True),
                Column('name', String(100), nullable=False, unique=True),
                Column('url', String(100), nullable=False, unique=True),
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
             Column('link', Text, nullable=False),
             Column('media', Text),
             Column('tags', Text)
             )


# check the list of resources in the database (tables "sources" and "source_urls") and the parser module (parsers.py)
def check_resource_list():
    list_url_sources = [i[0] for i in db_news.execute(select([sources.c.url])).fetchall()]

    for pars in parsers.list_parsers:
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


metadata.create_all(engine)

check_resource_list()

all_news = []

for parser in parsers.list_parsers:
    all_news.extend(parser['func_parser'](*parser['links_of_parse']))
    break

# print(*all_news, sep='\n')

r = db_news.execute(insert(news), all_news)
