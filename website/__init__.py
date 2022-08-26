from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from pathlib import Path
import os

db = SQLAlchemy()
DB_NAME = "encounters.db"

HOME_FOLDER = Path('.')
WEBSITE_FOLDER = HOME_FOLDER/"website"

load_dotenv()
SECRET_KEY = os.environ['SECRET_KEY']

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .views import views
    from .auth import auth
    from .models import User, Combat, Combatant

    create_db(app)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app

def create_db(app):

    if not Path.exists(WEBSITE_FOLDER/DB_NAME):
        db.create_all(app=app)
        print('Created Database')