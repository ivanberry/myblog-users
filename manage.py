# manage.py

import unittest
import coverage

from flask_script import Manager
from project import create_app, db
from project.api.models import User, Article
from flask_migrate import MigrateCommand

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*'
    ]
)

COV.start()

app = create_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """ Runs the tests without code coverage. """
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def recreate_db():
    '''Recreate a database'''
    db.drop_all()
    db.create_all()
    db.session.commit()

@manager.command
def seed_db():
    '''Seeds the database'''
    user_tab = User(username='tabxx', email='tabxx@gmail.com', password='test')
    user_shirting = User(username='shixrting', email='shirtixng@gmail.com', password='sss')
    db.session.add(user_tab)
    db.session.add(user_shirting)
    #db.session.add(Article(title='tabyy', body='Test', user_id=user_tab.id))
    #db.session.add(Article(title='shrating', body='test article', user_id=user_shirting))
    db.session.commit()

@manager.command
def cov():
    '''Run the unit tests with coverage.'''
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary: ')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1



if __name__ == '__main__':
    manager.run()
