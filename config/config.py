import os
from os.path import join, dirname
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
dotenv_path = join(dirname(dirname(__file__)), 'config.env')
load_dotenv(dotenv_path)

#ENTORNO
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')
HOST = os.getenv('DB_HOST')
PORT = os.getenv('DB_PORT')
DATABASE = os.getenv('DB_NAME')

class Config():
    SECRET_KEY = 'SECRET'
    DEBUG = True
    # Configuración de la base de datos SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


