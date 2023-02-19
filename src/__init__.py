from datetime import datetime
import os
import time
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from src import router
from src.config import appConfig

# db = SQLAlchemy()
# migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(appConfig.Config)
    # db.init_app(app)
    # migrate.init_app(app, db)
    app.register_blueprint(router.bluePrint)
    return app
