from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
import os


app = Flask(__name__, template_folder='templates')


temp_dir = os.environ.get("TMPDIR", "/tmp")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///comunidade.db"

app.config['SECRET_KEY'] = '91423650'

bcrypt = Bcrypt(app)
database = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'success'

from comunidade import routes

