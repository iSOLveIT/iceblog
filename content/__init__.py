from flask import Flask
# import urllib
from flask_pymongo import PyMongo
from flask_ckeditor import CKEditor
from flask_session import Session
# from flask_mail import Mail
# from flask_wtf.csrf import CSRFProtect
import os


# Instantiate flask and secret key
app = Flask(__name__)

# Instantiate csrf protection globally
# app.config['WTF_CSRF_ENABLED'] = True
# app.config['WTF_CSRF_SECRET_KEY'] = os.urandom(75)
# app.config['WTF_CSRF_FIELD_NAME'] = 'csrf_token'
# app.config['WTF_CSRF_TIME_LIMIT'] = 31536000
# csrf = CSRFProtect(app)

# Check Configuration section for more details
SESSION_COOKIE_NAME = "eveblog"
SESSION_COOKIE_PATH = "http://127.0.0.1:4700/admin_dashboard/"
SESSION_TYPE = 'filesystem'
SESSION_KEY_PREFIX = 'eve'
SESSION_FILE_DIR = "app_session"
PERMANENT_SESSION_LIFETIME = 86400
app.config.from_object(__name__)
Session(app)

"""
# Config and Instantiate Mongo
Username = urllib.parse.quote_plus('isolveit')
Password = urllib.parse.quote_plus('laden1472')
"""
app.config['MONGO_DBNAME'] = 'EVEBLOG'
app.config['MONGO_URI'] = "mongodb://localhost:27017/EVEBLOG"
mongo = PyMongo(app)

"""# Config Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = _mail_log['e-mail']
app.config['MAIL_PASSWORD'] = _mail_log['pswd']
app.config['MAIL_MAX_EMAILS'] = 1000

mail = Mail(app)
"""

# Config CKEDITOR
app.config['CKEDITOR_PKG_TYPE'] = 'full'
app.config['CKEDITOR_SERVE_LOCAL'] = True
ckeditor = CKEditor(app)

from content import url
