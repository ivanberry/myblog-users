# project/api/views.py

#framwork depes
from flask import Blueprint, jsonify, request, make_response
from sqlalchemy import exc

#project depes
from project.api.models import User, Article
from project import db
from project.api.utils import authenticate, is_admin, get_upload_token

import pdb

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@users_blueprint.route('/users', methods=['POST'])
@authenticate
def add_user(resp):
    # pdb.set_trace()
    if not is_admin(resp):
        response_object = {
            'status': 'error',
            'message': 'You do not have permission to do that.'
        }
        return make_response(jsonify(response_object)), 401
    post_data = request.get_json()
    # handler the empty post
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }

        # 返回
        return make_response(jsonify(response_object)), 400
    username = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('password')

    try:
        # handler the duplicate email post
        user = User.query.filter_by(email=email).first()

        # not duplicate email
        if not user:
            db.session.add(User(username=username, email=email, password=password))
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': f'{email} was added!'
            }
            return make_response(jsonify(response_object)), 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry, That email has already exist.'
            }
            return make_response(jsonify(response_object)), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return make_response(jsonify(response_object)), 400

    except ValueError as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }

        return make_response(jsonify(response_object)), 400


@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    '''Get single user details'''
    response_object = {
        'status': 'fail',
        'message': 'User does not exit'
    }

    try:
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            return make_response(jsonify(response_object)), 404
        else:

            response_object = {
                'status': 'success',
                'data': {
                    'username': user.username,
                    'email': user.email,
                    'created_at': user.created_at
                }
            }
            return make_response(jsonify(response_object)), 200
    except ValueError:
        return make_response(jsonify(response_object)), 404


@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
    '''Get all users'''
    users = User.query.order_by(User.created_at.desc()).all()
    users_list = []
    for user in users:
        user_object = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at
        }

        users_list.append(user_object)
    response_object = {
        'status': 'success',
        'data': {
            'users': users_list
        }
    }

    return make_response(jsonify(response_object)), 200


@users_blueprint.route('/articles', methods=['GET'])
def get_all_posts():
    '''Get all posts'''
    articles = Article.query.all()
    articles_list = []
    for article in articles:
        article_object = {
            'id': article.id,
            'title': article.title,
            'body': article.body,
            'pub_at': article.pub_at
        }

        articles_list.append(article_object)
    response_object = {
        'status': 'success',
        'data': {
            'articles': articles_list
        }
    }

    return make_response(jsonify(response_object)), 200

@users_blueprint.route('/articles/<user_id>', methods=['GET'])
def get_user_articles(user_id):
    '''Get or Post user's articles'''

    response_object = {
        'status': 'fail',
        'message': 'Cant find such user'
    }

    try:
        user = User.query.filter_by(id=int(user_id)).first()

        if not user:
            return make_response(jsonify(response_object)), 404
        else:
            articles = Article.query.filter_by(user_id=user.id).all()
            article_list = []

            for article in articles:
                article_object = {
                    'id': article.id,
                    'title': article.title,
                    'body': article.body,
                    'pub_at': article.pub_at,
                    'user_id': int(user_id)
                }

                article_list.append(article_object)

            response_object = {
                'status': 'success',
                'data': {
                    'articles': article_list
                }
            }

            return make_response(jsonify(response_object)), 200
    except ValueError:
        return make_response(jsonify(response_object)), 404

@users_blueprint.route('/articles', methods=['POST'])
def add_single_user_articles():
    post_data = request.get_json()

    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'invalid payload'
        }

        return make_response(jsonify(response_object)), 400

    user_id = post_data.get('user_id')

    if not user_id:
        response_object = {
            'status': 'fail',
            'message': 'invalid user'
        }
        return make_response(jsonify(response_object)), 404

    title = post_data.get('title')
    body = post_data.get('body')

    try:
        user = User.query.filter_by(id=int(user_id)).first()
        articles = Article.query.filter_by(user_id=int(user_id)).all()
        if not user:
            response_object = {
                'status': 'fail',
                'message': 'The user did not exist'
            }
            return make_response(jsonify(response_object)), 404
        else:
            db.session.add(Article(title=title, body=body, user_id=user_id))
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'The article has been added'
            }

            return make_response(jsonify(response_object)), 200
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'invalid payload'
        }
        return make_response(jsonify(response_object)), 400


