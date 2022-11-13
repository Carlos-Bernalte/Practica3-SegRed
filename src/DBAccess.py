'''Clase para conectar a la base de datos json y realizar las operaciones CRUD'''

import json
import os
import uuid
import hashlib
import base64
import jwt
import datetime

SECRET_KEY = 'secret'
class DBAccess:

    def __init__(self, db_name):
        self.db_name = db_name
        self.db = {}
        self.save_db()


    def hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    '''Crear un token que expira en 1 minuto'''
    def create_token(self, username):
        expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
        token = jwt.encode({'username': username, 'exp': expiration}, SECRET_KEY, algorithm='HS256')
        return token
    
    def verify_token(self, token):
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            expiration = datetime.datetime.fromtimestamp(data['exp'])
            if expiration < datetime.datetime.utcnow():
                raise jwt.ExpiredSignatureError
            return data
        except jwt.ExpiredSignatureError:
            return None

    def load_db(self):
        try:
            with open(self.db_name, 'r') as f:
                self.db = json.load(f)
        except FileNotFoundError:
            print('DB not found')
            exit(1)

    
    def save_db(self):
        with open(self.db_name, 'w') as f:
            json.dump(self.db, f, indent=4)
    

    def new_user(self, username, password):
        self.load_db()
        if username in self.db:
            return None
        self.db[username] = self.hash_password(password)
        self.save_db()
        return self.create_token(username)


    