# Local modules
import os
import ssl

# User-defined modules

# Third-party modules
from flask import Flask
from pymongo import MongoClient
from authlib.integrations.flask_client import OAuth
from flask_ckeditor import CKEditor
from flask_bcrypt import Bcrypt
from flask_compress import Compress
from flask_mail import Mail


# Instantiate flask and secret key
app = Flask(__name__)

# Session Configuration
SESSION_COOKIE_NAME = "ice_blog"
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
PERMANENT_SESSION_LIFETIME = 36000  # Expiration time for session (10 hours)

# Config and Instantiate Mongo
user = str(os.environ.get('MONGODB_USERNAME'))
passwd = str(os.environ.get('MONGODB_PASSWORD'))
uri = f"mongodb+srv://{user}:{passwd}@agms01-vtxt7.mongodb.net/?retryWrites=true&w=majority"    # Mongo connection str
client = MongoClient(uri, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)

mongo = client.get_database(name=str(os.environ.get('MONGO_DBNAME')))


# Auth0 configuration
AUTH0_CLIENT_ID = str(os.environ.get('AUTH0_CLIENT_ID'))
AUTH0_CLIENT_SECRET = str(os.environ.get('AUTH0_CLIENT_SECRET'))
AUTH0_CALLBACK_URL = str(os.environ.get('AUTH0_CALLBACK_URL'))
AUTH0_DOMAIN = str(os.environ.get('AUTH0_DOMAIN'))
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
PROFILE_KEY = str(os.environ.get('PROFILE_KEY'))
# Instantiate OAuth into app
oauth = OAuth(app)
# Register auth0
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

# Config Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_MAX_EMAILS'] = 1000

mail = Mail(app)


# Configure Flask Compress
# Types of files to compress
app.config['COMPRESS_MIMETYPES'] = ['text/html', 'text/css', 'text/javascript', 'application/javascript',
                                    'application/json', 'application/vnd.ms-fontobject',
                                    'image/svg+xml', 'font/ttf', 'font/woff', 'font/woff2']

Compress(app)  # Instantiate Flask Compress into app


# Bcrypt Configuration
bcrypt = Bcrypt(app)

# Config CKEDITOR
app.config['CKEDITOR_PKG_TYPE'] = 'full'
app.config['CKEDITOR_SERVE_LOCAL'] = True
ckeditor = CKEditor(app)


# Security measures
@app.after_request
def apply_headers(response):
    """
    Apply these security headers to the response sent by the server to the client,
    after a client has sent a request to the server
    Rules:
         * Strict-Transport-Security:
         * X-XSS-Protection:
         * X-Frame-Options:
         * Referrer-Policy:
         * Cache-Control:
         * X-Content-Type-Options:

    """
    response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubdomains; preload"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Cache-Control"] = "max-age=10368000"  # 4 months
    response.headers["X-Content-Type-Options"] = "nosniff"

    return response


from content import url
