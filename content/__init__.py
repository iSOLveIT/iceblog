from flask import Flask
from pymongo import MongoClient
from authlib.integrations.flask_client import OAuth
from flask_ckeditor import CKEditor
from flask_bcrypt import Bcrypt
from flask_compress import Compress
import os
import ssl


# Instantiate flask and secret key
app = Flask(__name__)

# Session Configuration
SESSION_COOKIE_NAME = "iceblog"
PERMANENT_SESSION_LIFETIME = 36000  # 10 hours

# Config and Instantiate Mongo
user = str(os.environ.get('MONGODB_USERNAME'))
pswd = str(os.environ.get('MONGODB_PASSWORD'))
uri = f"mongodb+srv://{user}:{pswd}@agms01-vtxt7.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)

mongo = client.get_database(name=str(os.environ.get('MONGO_DBNAME')))


# Auth0 configuration
AUTH0_CLIENT_ID = str(os.environ.get('AUTH0_CLIENT_ID'))
AUTH0_CLIENT_SECRET = str(os.environ.get('AUTH0_CLIENT_SECRET'))
AUTH0_CALLBACK_URL = str(os.environ.get('AUTH0_CALLBACK_URL'))
AUTH0_DOMAIN = str(os.environ.get('AUTH0_DOMAIN'))
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
PROFILE_KEY = str(os.environ.get('PROFILE_KEY'))

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=AUTH0_BASE_URL,
    access_token_url=AUTH0_BASE_URL + '/oauth/token',
    authorize_url=AUTH0_BASE_URL + '/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

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

# Bcrypt Configuration
bcrypt = Bcrypt(app)

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
    
    response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubdomains; preload"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Cache-Control"] = "max-age=10368000"  # 4 months

    return response

from content import url
