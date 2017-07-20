#project/api/utils.py

import os
from functools import wraps
from flask import request, make_response, jsonify
from project.api.models import User

from qiniu import Auth

import pdb

def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response_object = {
            'status': 'error',
            'message': 'Something went wrong. Please contact us.'
        }
        code = 401
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            response_object['message'] = 'Provide a valid auth token.'
            code = 403
            return make_response(jsonify(response_object)),  code
        auth_token = auth_header.split(' ')[1]
        resp = User.decode_auth_token(auth_token)
        if isinstance(resp, str):
            response_object['message'] = resp
            return make_response(jsonify(response_object)), code
        user = User.query.filter_by(id=resp).first()
        if not user or user.active:
            return make_response(jsonify(response_object)), code
        return f(resp, *args, **kwargs)
    return decorated_function

def is_admin(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user.admin

def get_upload_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        ak = 'FyG9hqVJz1p8EEinxZ95gESWd63kv4RMxBRrcleC'
        sk = os.environ.get('QINIU_SECRET_KEY')
        q = Auth(ak, sk)
        bucket_name='blog-article-images'
        policy = {
            'saveKey': '$(fname)',
            'mimeLimit': 'image/*',
            'fsizeLimit': 1024 * 1000
        }
        token = q.upload_token(bucket_name, None, 3600, policy)
        return f(token, *args, **kwargs)
    return decorated_function

