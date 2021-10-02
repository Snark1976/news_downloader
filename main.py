from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, DateTime, ForeignKey, Text
from datetime import datetime

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
             Column('title', Text, nullable=False),
             Column('source_id', Integer(), ForeignKey('sources.id')),
             Column('description', Text),
             Column('datetime', DateTime(), default=datetime.now),
             Column('url', Text, nullable=False),
             Column('media', Text),
             Column('tags', Text)
             )

metadata.create_all(engine)
