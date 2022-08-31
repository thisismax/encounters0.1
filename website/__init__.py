from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from pathlib import Path
import os

from flask_login import LoginManager

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

    from .views import views
    from .auth import auth
    from .models import User, Combat, Combatant

    db.init_app(app)

    create_db(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app

def create_db(app):

    if not Path.exists(WEBSITE_FOLDER/DB_NAME):
        db.create_all(app=app)
        print('Created Database')