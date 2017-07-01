#project/tests/test_model.py
from sqlalchemy.exc import IntegrityError

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.ultis import add_user

class TestUserModel(BaseTestCase):

    def test_add_user(self):
        user = add_user('test', 'test@gmail.com', 'test1')
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertTrue(user.password)
        self.assertTrue(user.active)
        self.assertTrue(user.created_at)

    def test_add_user_duppicate_username(self):
        add_user('test', 'test1@gmail.com', 'test')
        d_user = User(
            username='test',
            email='test@gmail.com',
            password='test'
        )
        db.session.add(d_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duppicate_emial(self):
        add_user('test', 'test@gmail.com', 'test')
        d_user = User(
            username='test1',
            email='test@gmail.com',
            password='test'
        )
        db.session.add(d_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_passwords_are_random(self):
        user_one = add_user('test@test.com', 'test@gmail.com', 'test')
        user_two = add_user('test@test2.com', 'test2@gmail.com', 'test')
        self.assertNotEqual(user_one.password, user_two.password)

    def test_encode_auth_token(self):
        user = add_user('test', 'tst@gmail.com', 'test')
        auth_token = user.encode_auth_token(user.id)
        # self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = add_user('test', 'ts@gmail.com', 'test')
        auth_token = user.encode_auth_token(user.id)
        # self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_user_token(auth_token), user_id)

