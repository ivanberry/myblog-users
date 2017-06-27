#project/tests/test_model.py
from sqlalchemy.exc import IntegrityError

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.ultis import add_user

class TestUserModel(BaseTestCase):

    def test_add_user(self):
        user = add_user('test', 'test@gmail.com')
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertTrue(user.active)
        self.assertTrue(user.created_at)

    def test_add_user_duppicate_username(self):
        add_user('test', 'test1@gmail.com')
        d_user = User(
            username='test',
            email='test@gmail.com'
        )
        db.session.add(d_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duppicate_emial(self):
        add_user('test', 'test@gmail.com')
        d_user = User(
            username='test1',
            email='test@gmail.com'
        )
        db.session.add(d_user)
        self.assertRaises(IntegrityError, db.session.commit)