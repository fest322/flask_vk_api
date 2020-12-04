from flask import Flask
from flask_login import LoginManager
from app import configurate

conf = configurate.Config('passwd.ini')
app = Flask(__name__)

app.config.update(
    DEBUG = True,
    SECRET_KEY = conf.getSetting('Flask', 'secure_key')
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from app import routes
