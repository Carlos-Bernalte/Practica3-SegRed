#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_restful import Api, Resource

from src.config import APP_NAME, APP_VERSION, SECRET_KEY
from src.persistance import DBAccess, FileSystem

app = Flask(APP_NAME)
api = Api(app)
db = DBAccess(SECRET_KEY)
fs = FileSystem()

class Version(Resource):
    def get(self):
        return {'version': APP_VERSION}

class Login(Resource):
    def post(self):
        data = request.get_json()
        if 'username' not in data or 'password' not in data:
            return {'error': 'Missing username or password'}, 400
            
        if data['username'] == "" or data['password']== "":
            return {'error': 'Invalid username or password'}, 400

        token = db.login(data['username'], data['password'])
        if token:
            return {'access_token': token}
        return {'error': 'Invalid username or password'}, 400

class Signup(Resource):
    def post(self):
        data = request.get_json()
        if 'username' not in data or 'password' not in data:
            return {'error': 'Missing username or password'}, 400

        if data['username'] == "" or data['password']== "":
            return {'error': 'Invalid username or password'}, 400
        
        if len(data['username'].split(' ')) > 1:
            return {'error': 'Invalid username'}, 400

        token = db.signup(data['username'], data['password'])

        if token:
            return {'access_token': token}, 201
        else:
            return {'error': 'username already exists'}, 400

class Docs(Resource):
    def get(self, username, doc_id):

        if not check_token(request.headers, username):
            return {'error': 'invalid token'}, 401

        result = fs.getFile(username, doc_id)
        if 'error' in result:
            return result, 404
        return result, 200

    def post(self, username, doc_id):
        if not check_token(request.headers, username):
            return {'error': 'invalid token'}, 401
        data = request.get_json()
        result=fs.newFile(username, doc_id, data['doc_content'])
        if 'error' in result:
            return result, 400
        return result, 201
    
    def put(self, username, doc_id):
        if not check_token(request.headers, username):
            return {'error': 'invalid token'}, 401

        result=fs.updateFile(username, doc_id, request.get_json()['doc_content'])
        if 'error' in result:
            return result, 400
        return result, 201

    def delete(self, username, doc_id):
        if not check_token(request.headers, username):
            return {'error': 'invalid token'}, 401
        result=fs.deleteFile(username, doc_id)
        if 'error' in result:
            return result, 400
        return result, 200
    

class AllDocs(Resource):
    def get(self, username):
        if not check_token(request.headers, username):
            return {'error': 'invalid token'}, 401
        
        return fs.getFiles(username), 200

def check_token(header, username):
    header=request.headers['Authorization'].split(' ')
    if header[0] == 'token':
        if db.verify_token(header[1], username):
            print('Existing token')
            return True
    return False

api.add_resource(Version, '/version')
api.add_resource(Login, '/login')
api.add_resource(Signup, '/signup')
api.add_resource(Docs, '/<string:username>/<string:doc_id>')
api.add_resource(AllDocs, '/<string:username>/_all_docs')

def run_app(host:int, port:str):
    try:
        app.run(
                host=host, 
                port=port, 
                debug=True, 
                ssl_context=('cert/myserver.local.crt', 'cert/myserver.local.key')
                )
    except FileNotFoundError:
        print('[ERROR] Certificado no encontrado')
    except Exception as e:
        print('[ERROR] ',e)
    
    

