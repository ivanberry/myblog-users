# project/api/auth.py

#framwork depes
from flask import Blueprint, jsonify, request, make_response
from sqlalchemy import exc, or_

#project depes
from project.api.models import User
from project import db, bcrypt
from project.api.utils import authenticate, get_upload_token

import pdb

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/auth/register', methods=['POST'])
def register_user():

    #get the post data
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'error',
            'message': 'Invalid payload.'
        }

        return make_response(jsonify(response_object)), 400
    username = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        #check for exiting user
        user = User.query.filter(or_(User.username == username, User.email == email)).first()
        if not user:
            #add user to db
            new_user = User(
                username=username,
                email=email,
                password=password
            )
            db.session.add(new_user)
            db.session.commit()

            #generate auth token and qiniu upload token that all included in JWT
            auth_token = new_user.encode_auth_token(new_user.id)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered',
                'auth_token': auth_token.decode()
            }
            return make_response(jsonify(response_object)), 201
        else:
            response_object = {
                'status': 'error',
                'message': 'Sorry, That user already exits.'
            }
            return make_response(jsonify(response_object)), 400

    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status': 'error',
            'message': 'Invalid payload.'
        }
        return make_response(jsonify(response_object)), 400
    except ValueError as e:
        db.session.rollback()
        response_object = {
            'status': 'error',
            'message': 'Invalid payload.'
        }
        return make_response(jsonify(response_object)), 400

@auth_blueprint.route('/auth/login', methods=['POST'])
def login_user():
    #get post data
    post_data = request.get_json()
    # pdb.set_trace()
    if not post_data:
        response_object = {
            'status': 'error',
            'message': 'Invalid payload.'
        }
        return make_response(jsonify(response_object)), 400
    email = post_data.get('email')
    password = post_data.get('password')

    try:
        #fetch data from db
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            user_token = user.encode_auth_token(user.id)
            if user_token:
                response_object = {
                    'status': 'success',
                    'message': 'Login success!',
                    'auth_token': user_token.decode()
                }
                return make_response(jsonify(response_object)), 200
        else:
            response_object = {
                'status': 'error',
                'message': 'User does not exsit.'
            }

            return make_response(jsonify(response_object)), 404
    except Exception as e:
        print(e)
        response_object = {
            'status': 'error',
            'message': 'Try again'
        }
        return make_response(jsonify(response_object)), 500

@auth_blueprint.route('/auth/logout', methods=['GET'])
@authenticate
def logout_user(resp):
    response_object = {
        'status': 'success',
        'message': 'Successfully logged out.'
    }

    return make_response(jsonify(response_object)), 200

@auth_blueprint.route('/auth/status', methods=['GET'])
@authenticate
def get_user_status(resp):
    user = User.query.filter_by(id=resp).first()
    response_object = {
        'status': 'success',
        'data': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'active': user.active,
            'created_at': user.created_at
        }
    }

    return make_response(jsonify(response_object)), 200





