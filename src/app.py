#!/usr/bin/env python3

import json

from flask import Flask, jsonify, request
from flask_restful import Api, Resource

from src.config import APP_NAME, APP_VERSION, DB_NAME, STORAGE_PATH
from src.persistance import DBAccess, FileSystem

app = Flask(APP_NAME)
api = Api(app)
db = DBAccess(DB_NAME)
fs = FileSystem(STORAGE_PATH)

class Version(Resource):
    def get(self):
        return {'version': APP_VERSION}

class Login(Resource):
    def post(self):
        data = request.get_json()
        if 'username' not in data or 'password' not in data:
            return {'error': 'Missing username or password'}, 400

        token = db.login(data['username'], data['password'])
        if token:
            return {'access_token': token}
        return {'error': 'Invalid username or password'}

class Signup(Resource):
    def post(self):
        data = request.get_json()
        if 'username' not in data or 'password' not in data:
            return {'error': 'Missing username or password'}, 400

        token = db.signup(data['username'], data['password'])
        if token:
            return {'access_token': token}
        else:
            return {'error': 'username already exists'}

class Docs(Resource):
    def get(self, username, doc_id):

        if not db.verify_token(request.headers['Authorization'], username):
            return {'error': 'invalid token'}

        doc_content = fs.getFile(username, doc_id)
        if doc_content is None:
            return {'error': 'File not found'}
        else:
            return doc_content

    def post(self, username, doc_id):
        if not db.verify_token(request.headers['Authorization'], username):
            return {'error': 'invalid token'}

        data = request.get_json()
        return fs.newFile(username, doc_id, data['doc_content'])
    
    def put(self, username, doc_id):
        if not db.verify_token(request.headers['Authorization'], username):
            return jsonify({'error': 'invalid token'})

        return fs.updateFile(username, doc_id, request.get_json()['doc_content'])

    def delete(self, username, doc_id):
        if not db.verify_token(request.headers['Authorization'], username):
            return {'error': 'invalid token'}
        return fs.deleteFile(username, doc_id)
    

class AllDocs(Resource):
    def get(self, username):
        if not db.verify_token(request.headers['Authorization'], username):
            return {'error': 'invalid token'}
        return fs.getFiles(username)

class Error(Resource):
    def get(self):
        return {'error': 'Invalid request'}


api.add_resource(Version, '/version')
api.add_resource(Login, '/login')
api.add_resource(Signup, '/signup')
api.add_resource(Docs, '/<string:username>/<string:doc_id>')
api.add_resource(AllDocs, '/<string:username>')



    

