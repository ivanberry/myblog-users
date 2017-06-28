#project/api/models.py

import datetime
import jwt
from project import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.String(255), nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False)
    articles = db.relationship('Article', backref='article', lazy='dynamic')

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

            return jwt.encode(
                    payload,
                    current_app.config.get('SECRET_KEY'),
                    algorithm='HS256'
            )
        except Exception as e:
            return e;


    def __init__(self, username, email, password, created_at=datetime.datetime.utcnow()):
        self.username = username
        self.email = email
        self.password = password
        self.created_at = created_at


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
