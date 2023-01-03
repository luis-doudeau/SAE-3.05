from flask import Flask
from secrets import token_urlsafe
from flask_login import LoginManager
from flask_principal import Principal, Permission, RoleNeed

app = Flask(__name__)
app.config['SECRET_KEY'] = token_urlsafe(16)

login_manager = LoginManager(app)
login_manager.login_view = 'connexion'

principals = Principal(app)

admin_permission = Permission(RoleNeed('admin'))