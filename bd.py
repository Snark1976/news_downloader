from sqlalchemy import create_engine


engine = create_engine("mysql+pymysql://root:Colobuc@localhost/news")
engine.connect()

print(engine)
