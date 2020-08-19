from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy_utils import create_database, database_exists

# Enter your postgres username and password
username = 'postgres'
password = 'postgres'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ebe6aecfada7f4cb575b702f62f26adb'

DB_URL = f'postgresql://{username}:{password}@localhost/toyproject'

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt()


if not database_exists(DB_URL):
    print('Creating Database')
    create_database(DB_URL)

from toyproject import routes
