from sqlalchemy import MetaData, Table, Column, String

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine , inspect

from urllib.parse import quote


from dotenv import load_dotenv
load_dotenv('.env')


from sqlalchemy import text

engine = create_engine("sqlite:///tst/main.db")
inspection = inspect(engine)
inspection.get_schema_names()
print(inspection.get_table_names())
# exit()
def add_column(engine, table_name, column):
    with engine.connect() as conn:
        column_name = column.compile(dialect=engine.dialect)
        column_type = column.type.compile(engine.dialect)
        conn.execute(text('ALTER TABLE %s ADD COLUMN %s %s' % (table_name, column_name, column_type)))

column = Column('new_column_name', String(100), primary_key=True)
tg_id_backup = Column('tg_id_backup', String, unique=True)

add_column(engine, 'files', tg_id_backup)
# Подключаемся к вашей базе данных
# with engine.begin() as conn:
#         conn.execute(
#                 text('''SELECT TABLE_NAME
# FROM INFORMATION_SCHEMA.TABLES''')
#         )
# metadata.tables.keys()
# # Используем MetaData для связи с существующей базой данных
# metadata = MetaData()

# # Определяем таблицу, к которой вы хотите добавить столбец
# users_table = Table('files', metadata, autoload=True)

# # Определяем новый столбец
# new_column = Column('tg_id_backup', String, unique=True)

# # Добавляем столбец к таблице
# new_column.create(users_table)