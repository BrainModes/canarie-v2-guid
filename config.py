import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    # info of postgresql database 
    PSQL_USERNAME = 'tokenizer'
    PSQL_PASSWORD = 'bX07rLZ5Fg'
    PSQL_DB = 'token'
    PSQL_HOST = 'psql_server'
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{PSQL_USERNAME}:{PSQL_PASSWORD}@{PSQL_HOST}/{PSQL_DB}'

    NBYTES = {'token08': 4,
              'token12': 6,
              'token16': 32,
              'token32': 64
    }

    LOGNAME = '/var/log/tokenizer.log'
    MBYTES = 10000000
    NFILES = 10000


