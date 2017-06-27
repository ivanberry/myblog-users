# project/__init__.py
import os
import datetime
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

# instantiate the db
db = SQLAlchemy()

# instantiate the migrate
migrate = Migrate()

def create_app():

    # instantiate the app
    app = Flask(__name__)

    #enable CORS
    CORS(app)

    # set config with docker env settings
    app_setting = os.getenv('APP_SETTINGS')
    app.config.from_object(app_setting)

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from project.api.views import users_blueprint
    app.register_blueprint(users_blueprint)

    return app



