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
            
        if data['username'] == "" or data['password']== "":
            return {'error': 'Invalid username or password'}, 400

        token = db.login(data['username'], data['password'])
        if token:
            return {'access_token': token}
        return {'error': 'Invalid username or password'}

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
        header=request.headers['Authorization'].split(' ')
        if header[0] == 'token':
            if not db.verify_token(header[1], username):
                return {'error': 'invalid token'}, 401


        doc_content = fs.getFile(username, doc_id)
        if doc_content is None:
            return {'error': 'File not found'} , 404
        else:
            return doc_content

    def post(self, username, doc_id):
        header=request.headers['Authorization'].split(' ')
        if header[0] == 'token':
            if not db.verify_token(header[1], username):
                return {'error': 'invalid token'}, 401

        data = request.get_json()
        return fs.newFile(username, doc_id, data['doc_content']), 201
    
    def put(self, username, doc_id):
        header=request.headers['Authorization'].split(' ')
        if header[0] == 'token':
            if not db.verify_token(header[1], username):
                return {'error': 'invalid token'}

        return fs.updateFile(username, doc_id, request.get_json()['doc_content']), 200

    def delete(self, username, doc_id):
        header=request.headers['Authorization'].split(' ')
        if header[0] == 'token':
            if not db.verify_token(header[1], username):
                return {'error': 'invalid token'}

        return fs.deleteFile(username, doc_id), 200
    

class AllDocs(Resource):
    def get(self, username):
        header=request.headers['Authorization'].split(' ')
        if header[0] == 'token':
            if not db.verify_token(header[1], username):
                return jsonify({'error': 'invalid token'}, 401)

        return fs.getFiles(username), 200


api.add_resource(Version, '/version')
api.add_resource(Login, '/login')
api.add_resource(Signup, '/signup')
api.add_resource(Docs, '/<string:username>/<string:doc_id>')
api.add_resource(AllDocs, '/<string:username>')

