#project/tests/ultis.py

import datetime
import os
from qiniu import Auth
from project import db
from project.api.models import User

def add_user(username, email, password, created_at=datetime.datetime.now()):
    user = User(
        username=username,
        email=email,
        password=password,
        created_at=created_at
    )

    db.session.add(user)
    db.session.commit()
    return user

def get_upload_token():
    ak = 'FyG9hqVJz1p8EEinxZ95gESWd63kv4RMxBRrcleC'
    sk = os.environ.get('QINIU_SECRET_KEY')
    q = Auth(ak, sk)
    bucket_name = 'blog-article-images'
    policy = {
        'saveKey': '$(fname)'
    }
    token = q.upload_token(bucket_name, None, 3600, policy)
    return token