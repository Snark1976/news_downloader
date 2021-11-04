import pymysql
from config import *


connection = pymysql.connect(host=host_db, user=name_user_db, password=password_user_db)

with connection:
    cursor = connection.cursor()
    cursor.execute(f'CREATE DATABASE {name_db}')
