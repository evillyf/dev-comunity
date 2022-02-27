from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)


#segurança contra ataques pelos forms
app.config['SECRET_KEY'] = '71234572572fbed270edec08df36c083'  #no terminal: python  >  import secrets > secrets.token_hex(16) >exit()
#banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pssilyckwdjvns:c757559a90b70b0a5f5ff92432c1e984c2a5c370623bf148cb964a21c59bbf9b@ec2-3-227-195-74.compute-1.amazonaws.com:5432/d1e2hkl27efku8'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please login to continue.'
login_manager.login_message_category = 'alert-info'

from comunidadeimpressionadora import routes
