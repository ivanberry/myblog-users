# project/api/auth.py

#framwork depes
from flask import Blueprint, jsonify, request, make_response
from sqlalchemy import exc, or_

#project depes
from project.api.models import User
from project import db, bcrypt

auth_blueprint = Blueprint('auth', __name__)

