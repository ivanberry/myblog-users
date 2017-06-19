# manage.py

import unittest
import coverage

from flask_script import Manager
from project import create_app, db
from project.api.models import User

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
    db.session.add(User(username='tab', email='tab@gmail.com'))
    db.session.add(User(username='shirting', email='shirting@gmail.com'))
    db.session.commit()

@manager.command
def cov():
    '''Run the unit tests with coverage.'''
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessfull():
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
