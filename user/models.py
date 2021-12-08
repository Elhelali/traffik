
from datetime import datetime, timedelta
import random,string,pymongo,jwt

from werkzeug.security import generate_password_hash,check_password_hash
from config import *
from flask import request,make_response,jsonify


class User:
    def create_user(database,name,email,password):
        user = {
                "id":''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(13)),
                "name":name,
                "email":email,
                "last_seen":datetime.utcnow(),
                "password": generate_password_hash(password)
            }
        users_db = database['users']
        users_db.insert_one(user)

    def login(database):
        users_db = database['users']
        auth = request.json

        if not auth or not auth['email'] or not auth['password']:
            # returns 401 if any email or / and password is missing
            response = make_response(
                'Could not verify',
                200,
                {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
            )
            response.headers.add("Access-Control-Allow-Credentials", "true")
            return response
        user = users_db.find_one({'email':auth['email']})
    
        if not user:
            # returns 401 if user does not exist
            return make_response(
                'Could not verify',
                200,
                {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
            )
        '''
        user = guard.authenticate(auth['email'], auth['password'])
        print(user)
        res = {'access_token': guard.encode_jwt_token(user)}
        return res, 200
        '''
        if check_password_hash(user['password'], auth['password']):
            # generates the JWT Token
            del user['_id']
            del user['password']
            del user['last_seen']
            token = jwt.encode({
                'id': user["id"],
                'user':user,
                'exp' : datetime.utcnow() + timedelta(minutes = 90) #30 minutes short time just to get the hang of things
            }, SECRET_KEY).decode('utf-8')
            
            response = make_response(jsonify({'token' : token, 'id':user["id"],'user':user}), 201)
            response.set_cookie('token', token, max_age=60*600)
            response.headers.add("Access-Control-Allow-Credentials", "true")
            return response
        # returns 403 if password is wrong
        
        return make_response(
            'Could not verify',
            403,
            {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
        )