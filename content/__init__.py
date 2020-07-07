from flask import Flask, request
# import urllib
from pymongo import MongoClient
from flask_ckeditor import CKEditor
from flask_session import Session
from flask_compress import Compress
import os

# Instantiate flask and secret key
app = Flask(__name__)

# Check Configuration section for more details
SESSION_COOKIE_NAME = "iceblog"
SESSION_COOKIE_PATH = "http://127.0.0.1:4700/admin_dashboard/"
SESSION_TYPE = 'filesystem'
SESSION_KEY_PREFIX = 'ice'
SESSION_FILE_DIR = "app_session"
PERMANENT_SESSION_LIFETIME = 86400  # 24 hours
app.config.from_object(__name__)
Session(app)

"""
# Config and Instantiate Mongo
Username = urllib.parse.quote_plus('isolveit')
Password = urllib.parse.quote_plus('laden1472')
"""
# Config and Instantiate Mongo
# user = str(os.environ.get('MONGODB_USERNAME'))
# pswd = str(os.environ.get('MONGODB_PASSWORD'))
# uri = f"mongodb+srv://{user}:{pswd}@agms01-vtxt7.mongodb.net/?retryWrites=true&w=majority"
# client = MongoClient(uri, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)

# Instantiate mongodb into app
client = MongoClient()
# app.config['MONGO_DBNAME'] = 'ICEBLOG'
mongo = client.get_database(name='EVEBLOG')

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

# Configure Flask Compress
app.config['COMPRESS_MIMETYPES'] = ['text/html', 'text/css', 'text/javascript', 'application/javascript',
                                    'application/json', 'application/vnd.ms-fontobject',
                                    'image/svg+xml', 'font/ttf', 'font/woff', 'font/woff2']

Compress(app)  # Instantiate Compress into app


# Security measures
@app.after_request
def apply_headers(response):
    # compression = request.headers["Accept-Encoding"]
    # algorithm = x if (x := 'br') in compression else 'gzip'
    # app.config['COMPRESS_ALGORITHM'] = algorithm  # configure compress algorithm

    response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubdomains; preload"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Cache-Control"] = "max-age=10368000"  # 4 months

    return response

from content import url
