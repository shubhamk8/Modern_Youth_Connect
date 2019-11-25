from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '48e2174d42e6715f7573dc3d4439e215'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # we pass the function name just like we do in the url_for
login_manager.login_message_category = 'info'
from Modern_Youth_Connect import routes
