#project/test/test_auth.py

import json
import time

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.ultis import add_user, get_upload_token

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
            self.assertIn('Invalid payload.', data['message'])
            self.assertTrue(response.status_code, 400)

    def test_registered_user_login(self):
        with self.client:
            user = add_user('test', 'test@gmail.com', 'test')
            response = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='test@gmail.com',
                    password='test'
                )),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Login success!')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.status_code, 200)

    def test_not_registered_user_login(self):
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='test@gmail.com',
                    password='test'
                )),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(data['message'] == 'User does not exsit.')
            self.assertTrue(response.status_code, 400)

    def test_invalid_user_login(self):
        with self.client:
            response = self.client.post(
                '/auth/login',
                data = json.dumps(dict()),
                content_type = 'application/json'
            )

            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(data['message'] == 'Invalid payload.')
            self.assertTrue(response.status_code, 400)

    def test_valid_logout(self):
        add_user('test', 'test@gmail.com', 'test')
        with self.client:
            #user login response
            resp_login = self.client.post(
                '/auth/login',
                data = json.dumps(dict(
                    email='test@gmail.com',
                    password='test'
                )),
                content_type = 'application/json'
            )

            #valid logout response
            response = self.client.get(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )

            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assertEqual(response.status_code, 200)

    def test_invalid_logout_expired_token(self):
        add_user('test', 'test@gmail.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data = json.dumps(dict(
                    email='test@gmail.com',
                    password='test'
                )),
                content_type='application/json'
            )

            # user invalid logout
            time.sleep(4)
            response = self.client.get(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )

            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(data['message'] == 'Signature expired. Please log in again')
            self.assertEqual(response.status_code, 401)

    def test_invalid_logout(self):
        with self.client:
            response = self.client.get(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer invalid'
                )
            )

            data = json.loads(response.data.decode())
            self.assertEqual(401, response.status_code)
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(data['message'] == 'Invalid token. Please log in again')

    def test_user_status(self):
        add_user('test', 'test@gmail.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data = json.dumps(dict(
                    email='test@gmail.com',
                    password='test'
                )),
                content_type='application/json'
            )

            response = self.client.get(
                '/auth/status',
                headers=dict(
                    Authorization='Bearer ' + json.loads(resp_login.data.decode())['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['username'] == 'test')
            self.assertTrue(data['data']['email'] == 'test@gmail.com')
            self.assertTrue(data['data']['active'] == False)
            self.assertTrue(data['data']['created_at'])
            self.assertEqual(response.status_code, 200)

    def test_user_invalid_status(self):
        with self.client:
            response = self.client.get(
                '/auth/status',
                headers=dict(
                    Authorization='Bearer invalid'
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(
                data['message'] == 'Invalid token. Please log in again'
            )
            self.assertEqual(response.status_code, 401)

    def test_invalid_logout_inactive(self):
        add_user('test', 'test@gmail.com', 'test')
        #update_user
        user = User.query.filter_by(email='test@gmail.com').first()
        user.active = True
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data = json.dumps(dict(
                    email='test@gmail.com',
                    password='test'
                )),
                content_type = 'application/json'
            )

            response = self.client.get(
                '/auth/logout',
                headers = dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )

            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(data['message'] == 'Something went wrong. Please contact us.')
            self.assertEqual(response.status_code, 401)

    # def test_upload_token(self):
    #     '''Ensure get token correctly'''
    #     add_user('test', 'test@gmail.com', 'test')
    #
    #     with self.client:
    #         resp_login = self.client.post(
    #             '/auth/login',
    #             data = json.dumps(dict(
    #                 email='test@gmail.com',
    #                 password='test'
    #             )),
    #             content_type = 'application/json'
    #         )
    #
    #         response = self.client.get(
    #             '/auth/qiniu',
    #             headers = dict(
    #                 Authorization='Bearer ' + json.loads(
    #                     resp_login.data.decode()
    #                 )['auth_token']
    #             )
    #         )
    #
    #         data = json.loads(response.data.decode())
    #         self.assertTrue(response.status_code, 200)
    #         self.assertTrue(data['status'], 'success')
    #         self.assertTrue(data['q_token'])













