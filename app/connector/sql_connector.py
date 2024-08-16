from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_TYPE = os.getenv('TYPE')
DATABASE_HOST = os.getenv('HOST_DB')
DATABASE_NAME = os.getenv('NAME_DB')
DATABASE_PORT = os.getenv('PORT')
DATABASE_USER = os.getenv('USER')
DATABASE_PASSWORD = os.getenv('PASSWORD')

print('Connecting to SQL Server')

engine = create_engine(f'{DATABASE_TYPE}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')

connection = engine.connect()
Session = sessionmaker(connection)

print(f'connected to sql database {DATABASE_HOST}')
