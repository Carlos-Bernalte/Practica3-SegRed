#!/usr/bin/env python3

import json

from flask import Flask, jsonify, request
from flask_restful import Api, Resource

from src.config import APP_NAME, APP_VERSION, DB_NAME
from src.DBAccess import DBAccess

app = Flask(APP_NAME)
api = Api(app)
db = DBAccess(DB_NAME)

class Version(Resource):
    def get(self):
        return {'version': APP_VERSION}

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        token = db.new_user(username, password)
        if token:
            return {'token': token}
        else:
            return {'error': 'username already exists'}

class Signup(Resource):
    def post(self):
        autorization = request.authorization
        print('Autorización: ', autorization)
        token = request.headers.get('token')
        db.verify_token(token)
        if db.verify_token(token) is None:
            return {'error': 'Token expired'}
        print(token)
        data = request.get_json()
        print(data)
        return {'status':'ok'}

class Docs(Resource):
    def get(self):
        return {'status':'ok'}

    def post(self, username, doc_id):
        print(username, doc_id)
        data = request.get_json()
        db.set(username, data)
        return {'status':'ok'}
    
    def put(self, username, doc_id):
        data = request.get_json()
        db.set(username, data)
        return {'status':'ok'}
    
    def delete(self, username, doc_id):
        db.delete(username, doc_id)
        return {'status':'ok'}
    
    def get(self, username):
        return {'status':'get all'}


api.add_resource(Version, '/version')
api.add_resource(Login, '/login')
api.add_resource(Signup, '/signup')
api.add_resource(Docs, '/<string:username>/<string:doc_id>', '/<string:username>/all_docs')




    

