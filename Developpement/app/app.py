from flask import Flask
from secrets import token_urlsafe
from flask_login import LoginManager
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SECRET_KEY'] = token_urlsafe(16)

login_manager = LoginManager(app)
login_manager.login_view = 'connexion'

mail = Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'bdboum45@gmail.com'
app.config['MAIL_PASSWORD'] = 'llmbdboum'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

