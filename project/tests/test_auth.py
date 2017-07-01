#project/test/test_auth.py

import json

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.ultis import add_user