from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.environ['SECRET_KEY']

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app