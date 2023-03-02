from flask import Flask
from secrets import token_urlsafe
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = token_urlsafe(16)

login_manager = LoginManager(app)
login_manager.login_view = 'connexion'


<<<<<<< HEAD
#bdboum45@gmail.com
=======
app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'bdboum45@gmail.com'
#app.config['MAIL_PASSWORD'] = 'llmbdboum'
app.config['MAIL_PASSWORD'] = 'otpvlohopdtlvrjz'
#app.config['TESTING'] = False
#app.config['MAIL_USE_TLS'] = False
#app.config['MAIL_USE_SSL'] = True

>>>>>>> detail_navette
#llmbdboum1234567