from datetime import datetime
import os
import time
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from src import router
from src.config import appConfig
import threading
from src.services import mailTodaysContests 

# db = SQLAlchemy()
# migrate = Migrate()

send_from = 'khssupriya@gmail.com'
send_to = ['contest-scraper-instagram@googlegroups.com']

def getContests():
    while True:
        now = datetime.now().strftime("%H")
        print(now)
        if now == "07":
            mailTodaysContests(send_from, send_to)
        time.sleep(60)
    

def create_app():
    threading.Thread(target=getContests).start()
    app = Flask(__name__)
    app.config.from_object(appConfig.Config)
    # db.init_app(app)
    # migrate.init_app(app, db)
    app.register_blueprint(router.bluePrint)
    return app
