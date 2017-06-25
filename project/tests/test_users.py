# project/tests_users.py

import json
from project.tests.base import BaseTestCase
from project import db
from project.api.models import User, Article
import datetime

def add_user(username, email, created_at=datetime.datetime.now()):
    user = User(username=username, email=email, created_at=created_at)
    db.session.add(user)
    db.session.commit()
    return user

def add_article(title, body, pub_at=datetime.datetime.utcnow()):
    article = Article(title=title, body=body, pub_at=pub_at)
    db.session.add(article)
    db.session.commit()
    return article

class TestUsersService(BaseTestCase):
    '''Tests for the Users Services'''

    def test_users(self):
        '''Ensure the /ping route behaviors correctly'''
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        '''Ensure a new user can be added to the database'''

        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    username = 'tab',
                    email='tab@gmail.com'
                )),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('tab@gmail.com was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        '''Ensure error is thrown if the JSON object is empty'''
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict()),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        '''Ensure error is thrown if the JSON object does not have username key'''
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(emai='tab@gmail.com')),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_user(self):
        '''Ensure error is thrown if the email already exits.'''
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='tab',
                    email='tab@gmail.com'
                )),
                content_type='application/json'
            )

            # 模拟post请求，绑定'users'接口返回的数据
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='shrint',
                    email='tab@gmail.com'
                )),
                content_type='application/json'
            )

            # 解码返回的数据
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry, That email has already exist.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        '''Ensures get single user behaves correctly'''

        # add user first
        user = add_user('tab', 'tab@gmail.com')

        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('created_at' in data['data'])
            self.assertIn('tab', data['data']['username'])
            self.assertIn('tab@gmail.com', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        '''Ensures error is thrown if an id is not provided'''
        with self.client:
            response = self.client.get(f'/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exit', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_incorrect_id(self):
        '''Ensure incorrect id is thrown if '''
        with self.client:
            response = self.client.get(f'/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exit', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        '''Ensure get all users behaviors correctly'''
        created = datetime.datetime.now() + datetime.timedelta(-30)
        add_user('tab', 'tab@gmail.com', created)
        add_user('shirting', 'shirting@gmail.com')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertTrue('created_at' in data['data']['users'][0])
            self.assertTrue('created_at' in data['data']['users'][1])
            self.assertIn('tab', data['data']['users'][1]['username'])
            self.assertIn('tab@gmail.com', data['data']['users'][1]['email'])
            self.assertIn('shirting', data['data']['users'][0]['username'])
            self.assertIn('shirting@gmail.com', data['data']['users'][0]['email'])
            self.assertIn('success', data['status'])


class TestArticlesService(BaseTestCase):
    def test_all_articles(self):
        '''Ensure get all articles correctly'''
        add_article('test', 'This is a test content')
        add_article('test2', 'This is a another test content')
        with self.client:
            response = self.client.get('/articles')
            data = json.loads(response.data.decode())

            # asserts
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])

            # 数据条数
            self.assertEqual(len(data['data']['articles']), 2)

            # 返回是否包含created_at
            self.assertTrue('pub_at' in data['data']['articles'][0])
            self.assertTrue('pub_at' in data['data']['articles'][1])

            # 对应的article是否在返回数据中
            self.assertTrue('test' in data['data']['articles'][0]['title'])
            self.assertIn('This is a test content', data['data']['articles'][0]['body'])
            self.assertTrue('test2' in data['data']['articles'][1]['title'])
            self.assertIn('This is a another test content', data['data']['articles'][1]['body'])




































