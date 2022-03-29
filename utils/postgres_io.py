import sys
import logging
import datetime
import psycopg2
from sqlalchemy import create_engine,types
import pandas as pd


class PostgresIO:

    def __init__(self, dbname, username, password, host='localhost', port=5432, timeout=1800, logger=None):
        self.db = dbname
        self.user = username
        self.pwd = password
        self.host = host
        self.timeout = timeout
        self.conn = f'postgresql://{username}:{password}@{host}:{port}/{dbname}'
        if logger is not None:
            self.logger = logger
        else:
            logging.basicConfig(stream=sys.stdout, level=logging.INFO)
            self.logger = logging.getLogger()

    def read_table(self, table, cond=''):
        engine = create_engine(self.conn)
        self.logger.info(f'read table {table} with {cond}')
        df = pd.read_sql_query(f'select * from {table} {cond}',con=engine)
        return df

    def insert_to_table(self, table, df, mode='append', index=False, json_col=None):
        engine = create_engine(self.conn)
        self.logger.info(f'{mode} table {table}')
        if json_col:
            dtype = {}
            for col in json_col: dtype[col] = types.JSON
            df.to_sql(table, engine,  if_exists=mode, index=index, dtype=dtype)
        else:
            df.to_sql(table, engine,  if_exists=mode, index=index)
        self.logger.info(f'{mode} done.')

    def update_table(self, table, ref_table, match, set_):
        self.logger.info(f'update table {table} using {ref_table}')
        engine = create_engine(self.conn)
        cols = ','.join(match)
        command = f'insert into {table} ({cols}) select {cols} from {ref_table} where ({cols}) not in (select {cols} from {table});'
        self.logger.info(f'excuting command: {command}.')
        with engine.connect() as connection:
            result = connection.execute(command)
        self.logger.info(f'done.')
            
        cols_set = ','.join([f'{c}={ref_table}.{c}' for c in set_])
        cols_join = ' and '.join([f'{table}.{c}={ref_table}.{c}' for c in match])
        command = f'update {table} set {cols_set} from {ref_table} where {cols_join} ;'
        self.logger.info(f'excuting command: {command}.')
        with engine.connect() as connection:
            result = connection.execute(command)
        self.logger.info(f'done.')
