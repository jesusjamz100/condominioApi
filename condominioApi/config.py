import os
from dotenv import load_dotenv

load_dotenv()

class BaseConfig(object):
    ''' Basic configuration of the API '''

    # Configuracion principal
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = False
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')

class DevelopmentConfig(BaseConfig):
    # Configuracion del entorno de desarrollo
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///condominio.db'