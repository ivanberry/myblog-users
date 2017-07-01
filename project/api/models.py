#project/api/models.py

import datetime
import jwt
from flask import current_app
from project import db, bcrypt

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.String(255), nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False)
    articles = db.relationship('Article', backref='article', lazy='dynamic')

    def __init__(self, username, email, password, created_at=datetime.datetime.utcnow()):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(
                password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        )
        self.created_at = created_at

    @staticmethod
    def decode_auth_token(auth_token):
        '''Decode auth token'''
        try:
            payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again'


    def encode_auth_token(self, user_id):
        '''Generate user auth token'''
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=current_app.config.get('TOKEN_EXPIRATION_DAYS'),
                    seconds=current_app.config.get('TOKEN_EXPIRATION_SECONDS')
                ),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }

            user_token = jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )

            return user_token

        except Exception as e:
            return e




class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_at = db.Column(db.DateTime, nullable=False)
    update_at = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, body, user_id, pub_at=datetime.datetime.utcnow()):
        self.title = title
        self.body = body
        self.user_id = user_id
        self.pub_at = pub_at
