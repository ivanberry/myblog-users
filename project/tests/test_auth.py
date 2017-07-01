#project/test/test_auth.py

import json

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.ultis import add_user

class TestAuthBlueprint(BaseTestCase):
    def test_user_register(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data = json.dumps(dict(
                    username='test@test.com',
                    email='test@gmail.com',
                    password='test'
                )),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertTrue(response.status_code == 201)

    def test_user_register_duplicate_email(self):

        add_user('test', 'test@gmail.com', 'test')

        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    username='test1',
                    email='test@gmail.com',
                    password='test0'
                )),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(data['message'] == 'Sorry, That user already exits.')
            self.assertTrue(response.status_code == 400)

    def test_user_register_duplicate_username(self):
       add_user('test', 'test0@gmail.com', 'test')

       with self.client:
           response = self.client.post(
               '/auth/register',
               data = json.dumps(dict(
                   username='test',
                   email='test@gmail.com',
                   password='test0'
               )),
               content_type='application/json'
           )

           data = json.loads(response.data.decode())
           self.assertTrue(data['status'] == 'error')
           self.assertTrue(data['message'] == 'Sorry, That user already exits.')
           self.assertTrue(response.status_code == 400)

    def test_user_register_invalid_json(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data = json.dumps(dict()),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(data['message'] == 'Invalid payload.')
            self.assertTrue(response.status_code == 400)

    def test_user_register_invalid_json_without_username(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data = json.dumps(dict(
                    email='test@gmail.com',
                    password='test'
                )),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertIn('Invalid payload.', data['message'])
            self.assertTrue(response.status_code, 400)

    def test_user_register_invalid_json_without_email(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data = json.dumps(dict(
                    username='test',
                    password='test'
                )),
                content_type='application/josn'
            )

            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(data['message'] == 'Invalid payload.')
            self.assertTrue(response.status_code, 400)

    def test_user_register_invalid_json_without_pw(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data = json.dumps(dict(
                    username='test',
                    email='test@gmail.com'
                )),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())
            self.assertTrue('error', data['status'])
            self.assertTrue('Invalid payload.', data['message'])
            self.assertTrue(response.status_code, 400)




