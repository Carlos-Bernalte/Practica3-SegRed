'''Clase para conectar a la base de datos json y realizar las operaciones CRUD'''

import json
import os
import uuid
import hashlib
import base64
import jwt
import datetime
from dotenv import load_dotenv

load_dotenv()


class DBAccess:

    def __init__(self, db_name):
        self.db_name = db_name
        self.db = {}
        self.save_db()
        self.tokens = {}
        self.load_db()
        self.save_db()
        self.key = os.getenv('SECRET_KEY')
    '''Hashear la contraseña con un salt en base a el username'''

    def hash_password(self, username,password):
        salt = username.encode('utf-8')
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return base64.b64encode(salt + key).decode()
        
    '''Crear un token que expira en 1 minuto'''
    def create_token(self, username):
        expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        token = jwt.encode({'username': username, 'exp': expiration}, self.key, algorithm='HS256')
        return token


    def verify_token(self, token, username):
        
        try:
            data = jwt.decode(token, self.key, algorithms=['HS256'])
            expiration = datetime.datetime.fromtimestamp(data['exp'])
            if expiration < datetime.datetime.utcnow():
                print('Token expired')
                raise jwt.ExpiredSignatureError
            if data['username'] != username:
                print('Usuario no coincide con el token')
                raise jwt.InvalidTokenError
            if not self.confirm_token(token, username):
                raise jwt.InvalidTokenError
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
            
    def confirm_token(self, token, username):
        self.load_db()
        if username in self.db:
            if self.tokens[username]== token:
                return True
        return False

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
    

    def signup(self, username, password):
        self.load_db()
        if username in self.db:
            return None
        token = self.create_token(username)  
        self.db[username] = self.hash_password(username,password)
        self.tokens[username]= token
        self.save_db()
        return token

    def login(self, username, password):
        self.load_db()
        if username in self.db:
            if self.db[username]== self.hash_password(username,password):
                token = self.create_token(username)
                self.tokens[username]= token
                self.save_db()
                return token
        return None

class FileSystem:

    def __init__(self, path):
        self.path = path
        os.makedirs(self.path, exist_ok=True)

    def newFile(self, username, doc_id, data):
        if not self.file_exists(username, doc_id):
            os.makedirs(os.path.join(self.path, username), exist_ok=True)
            with open(os.path.join(self.path, username, doc_id), 'w') as f:
                f.write(data)
            return {'size': os.path.getsize(os.path.join(self.path, username, doc_id))}
        return {'error': 'File already exists'}

    def deleteFile(self, username, doc_id):
        if self.file_exists(username, doc_id):
            os.remove(os.path.join(self.path, username, doc_id))
            return {}
        return {'error': 'File not found'}


    '''Devolver el contenido de todos los archivos de un usuario'''
    def getFiles(self, username):
        all_files = {}
        for root, dirs, files in os.walk(os.path.join(self.path, username)):
            for name in files:
                with open(os.path.join(root, name), 'r') as f:
                    all_files[name] = {'doc_content':f.read()}
        return all_files
    '''Devolver el contenido del archivo en formato JSON'''
    def getFile(self, username, doc_id):
        if self.file_exists(username, doc_id):
            with open(os.path.join(self.path, username, doc_id), 'r') as f:
                return {'doc_content': f.read()}
        return {'error': 'File not found'}
    
    def updateFile(self, username, doc_id, data):
        if self.file_exists(username, doc_id):
            with open(os.path.join(self.path, username, doc_id), 'w') as f:
                f.write(data)
            return {'size': os.path.getsize(os.path.join(self.path, username, doc_id))}
        return {'error': 'File not found'}


    def file_exists(self, username, doc_id):
        return os.path.isfile(os.path.join(self.path, username, doc_id))

    

    