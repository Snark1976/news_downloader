from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, DateTime, ForeignKey, Text, insert
from datetime import datetime
import parsers

metadata = MetaData()

engine = create_engine("mysql+pymysql://root:Colobuc@localhost/db_news", echo=True)


sources = Table('sources', metadata,
                Column('id', Integer(), primary_key=True),
                Column('name', String(30), nullable=False),
                Column('url', String(50), nullable=False),
                Column('description', String(100), nullable=False)
                )

source_urls = Table('source_urls', metadata,
                    Column('id', Integer(), primary_key=True),
                    Column('source_id', Integer(), ForeignKey('sources.id'))
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

metadata.create_all(engine)

db_news = engine.connect()

all_news = []

for url, parser in parsers.dict_parsers.items():
    all_news.extend(parser(url))
    break

print(*all_news, sep='\n')

r = db_news.execute(insert(news), all_news)
print(r)
