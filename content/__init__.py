from flask import Flask
import urllib
from flask_pymongo import PyMongo
from flask_ckeditor import CKEditor
from flask_mail import Mail


# Instantiate flask and secret key
app = Flask(__name__)
app.secret_key = '679fbfedf3ca6ac21c07d2e175314c7e2bd543ebcdd8ad'

"""
# Config and Instantiate Mongo
Username = urllib.parse.quote_plus('isolveit')
Password = urllib.parse.quote_plus('laden1472')
"""
app.config['MONGO_DBNAME'] = 'Blog'
app.config['MONGO_URI'] = "mongodb+srv://%s:%s@mfilx-hw1xz.mongodb.net/Blog" % (Username, Password)
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
ckeditor = CKEditor(app)

from content import url
