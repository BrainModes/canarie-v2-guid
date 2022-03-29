from flask.views import MethodView
from flask import jsonify, request, abort
from secrets import token_hex, randbelow
import pandas as pd 
from sqlalchemy import exc

from config import Config as conf
from utils.postgres_io import PostgresIO


class TokenAPI(MethodView):

    def __init__(self):
        self.db = PostgresIO(conf.PSQL_DB, conf.PSQL_USERNAME, 
                            conf.PSQL_PASSWORD, conf.PSQL_HOST)

    def key_gen(self, table, key, n=6):
        val = None
        while not val:
            cur = token_hex(n)
            print(table, key, cur, n)
            df = pd.DataFrame([[key, cur]], columns=['key', 'value'])
            try:
                self.db.insert_to_table(table, df)
            except exc.IntegrityError as err:
                print("token collids")
            df = self.db.read_table(table, f"where key='{key}'") 
            if df.shape[0] == 1:
                val = df.value[0]
        return val

    def get(self, table, key):
        val = None
        df = self.db.read_table(table, f"where key='{key}'")
        if df.shape[0] == 1:
            val = df.value[0]
        else:
            val = self.key_gen(table, key, conf.NBYTES.get(table, 6))
        return jsonify({key: val}), 200
        

class TokenAPI_2Keys(MethodView):

    def __init__(self):
        self.db = PostgresIO(conf.PSQL_DB, conf.PSQL_USERNAME, 
                            conf.PSQL_PASSWORD, conf.PSQL_HOST)

    def key_gen(self, table, userID, projID, n=6):
        val = None
        while not val:
            cur = token_hex(n)
            print(table, userID, projID, cur, n)
            df = pd.DataFrame([[userID, projID, cur]], columns=['userid', 'projid', 'guid'])
            try:
                self.db.insert_to_table(table, df)
            except exc.IntegrityError as err:
                print("token collids")
            df = self.db.read_table(table, f"where USERID='{userID}' and PROJID='{projID}'") 
            if df.shape[0] == 1:
                val = df.guid[0]
        return val

    def get(self, table):
        userID = request.args.get('userid')
        projID = request.args.get('projid')
        val = None
        df = self.db.read_table(table, f"where USERID='{userID}' and PROJID='{projID}'")
        if df.shape[0] == 1:
            val = df.guid[0]
        else:
            val = self.key_gen(table, userID, projID, conf.NBYTES.get(table, 6))
        return jsonify({'guid': val, 'userID': userID, 'projID': projID}), 200
        

class TokenAPI_digits(MethodView):
    '''
    giving two keys, generate a random integer of 15 digits
    '''
    def __init__(self):
        self.db = PostgresIO(conf.PSQL_DB, conf.PSQL_USERNAME, 
                            conf.PSQL_PASSWORD, conf.PSQL_HOST)

    def key_gen(self, table, userID, projID, n=15):
        val = None
        while not val:
            cur = f'{randbelow(10**n):015}'
            print(table, userID, projID, cur, len(cur))
            df = pd.DataFrame([[userID, projID, cur]], columns=['userid', 'projid', 'guid'])
            try:
                self.db.insert_to_table(table, df)
            except exc.IntegrityError as err:
                print("token collids")
            df = self.db.read_table(table, f"where USERID='{userID}' and PROJID='{projID}'") 
            if df.shape[0] == 1:
                val = df.guid[0]
        return val

    def get(self, table):
        userID = request.args.get('userid')
        projID = request.args.get('projid')
        val = None
        df = self.db.read_table(table, f"where USERID='{userID}' and PROJID='{projID}'")
        if df.shape[0] == 1:
            val = df.guid[0]
        else:
            val = self.key_gen(table, userID, projID, conf.NBYTES.get(table,15))
        return jsonify({'guid': val, 'userID': userID, 'projID': projID}), 200
        
                                