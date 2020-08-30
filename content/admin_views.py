from flask.views import MethodView
from flask import render_template, redirect, request, url_for, flash, session
from content import mongo, app, bcrypt, auth0, AUTH0_CALLBACK_URL, AUTH0_CLIENT_ID, PROFILE_KEY
from bson.objectid import ObjectId
from .form import ArticleForm, SignupForm
from datetime import datetime as dt
from functools import wraps
from pymongo import DESCENDING
from emoji import emojize
from six.moves.urllib.parse import urlencode
from .commentIDgenerator import random_string


# Check if user is logged in
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if PROFILE_KEY not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated


# View for login
class AdminLoginEndpoint(MethodView):
    @staticmethod
    def get():
        # Redirects app to the callback url (i.e. the apps auth0 login link)
        # After the user has entered login details,
        # if details are correct an authorized access token is sent to the apps
        # callback handler by auth0
        return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL)


# View for callback
class CallbackHandler(MethodView):
    @staticmethod
    def get():
        # Get data (access_token and user_info) from auth0
        auth0.authorize_access_token()
        auth0_response = auth0.get('userinfo')
        
        # Retrieve json from data sent by auth0
        user_info = auth0_response.json()

        # Create session object (dict_object) and store data in session
        session['logged_in'] = True
        session[PROFILE_KEY] = {
            'user_id': str(user_info['sub']).split('|')[1],
            'username': str(user_info['nickname']),
            'firstName': str(user_info['name'].split(' ')[0]),
            'lastName': str(user_info['name'].split(' ')[1]),
            'gender': str(user_info['gender']),
            'picture': str(user_info['picture'])
        }
        
        flash(f"Logged in successfully {emojize(':grinning_face_with_big_eyes:')}", 'success')
        return redirect(url_for('dashboard'))
            

# View for admin dashboard
class AdminDashboardEndpoint(MethodView):
    @staticmethod
    # @requires_auth
    def get():
        # Create Mongodb connection
        articles = mongo.get_collection(name='articles')
        # Get user information stored in session
        user_info = session.get(PROFILE_KEY)
        # Get username from user info
        author = user_info['username']
        # Execute query to fetch data from database
        posts = articles.find({"author": author}).sort('datePosted', DESCENDING)
        return render_template('admin.html', others=False, posts=posts, user_info=user_info)


# View for admin logout
class AdminLogoutEndpoint(MethodView):
    @staticmethod
    # @requires_auth
    def get():
        session.clear()     # Clear all data in session
        params = {'returnTo': url_for('index', _external=True), 'client_id': AUTH0_CLIENT_ID}
        # Logout user and redirect user to homepage
        return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))
        

# View for admin account details
class AdminProfileEndpoint(MethodView):
    @staticmethod
    # @requires_auth
    def get():
        # Create Mongodb connection
        users = mongo.get_collection(name='admin_user')
        # Get user information stored in session and get only username
        username = session.get(PROFILE_KEY)['username']
        # Execute query to fetch only one data
        user_details = users.find_one({'username': username})
        return render_template('admin_profile.html', others=False, user=user_details)

    @staticmethod
    # @requires_auth
    def post():
        # Create Mongodb connection
        users = mongo.get_collection(name='admin_user')

        # Receive inputs sent through forms
        last_name = str(request.form['LName'])
        first_name = str(request.form['FName'])
        email = str(request.form['Email'])
        gender = str(request.form['Gender'])
        bio = str(request.form['bio'])

        # Hash (encrypt) password
        # encrypted_password = bcrypt.generate_password_hash(str(password), rounds=10).decode('utf-8')

        # Get user information stored in session and get only username
        username = session.get(PROFILE_KEY)['username']
        session[PROFILE_KEY]['lastName'] = last_name
        session[PROFILE_KEY]['firstName'] = first_name
        session[PROFILE_KEY]['gender'] = gender
        session.modified = True
        # Execute query to find and update data
        users.find_one_and_update(
            {'username': username},
            {
                '$set': {
                    'lastName': last_name, 'firstName': first_name,
                    'email': email, 'gender': gender,
                    'biography': bio, 'dateModified': dt.now()
                }
            },
            upsert=False,
        )
        flash(f"Account details updated {emojize(':grinning_face_with_big_eyes:')}", 'success')
        return redirect(url_for('profile'))


# View for add article
class AddArticleEndpoint(MethodView):
    @staticmethod
    # @requires_auth
    def get():
        form = ArticleForm(request.form)
        return render_template('add_article.html', others=False, form=form)

    @staticmethod
    # @requires_auth
    def post():
        # Create Mongodb connection
        articles = mongo.get_collection(name='articles')

        # Receive inputs sent through forms
        slug = str(random_string())
        title = str(request.form['title']).upper()
        keywords = str(request.form['keywords'])
        body = str(request.form['body'])
        category = str(request.form['category'])
        read_time = str(request.form['readTime'])
        author = str(session.get(PROFILE_KEY)['username'])   # Get user info stored in session and get only username
        image_in_jpg_received = str(request.form['jpg_cover'])
        image_in_webp_received = str(request.form['webp_cover'])
        image_alt_text = str(request.form['image_alt_text'])
        status = str(request.form.get('status', 'draft'))
        body_updated = False

        # Replace some parts of the string (links for the image)
        # This will help us render the image on our website
        jpg_image_id = image_in_jpg_received.split('/')[5]
        webp_image_id = image_in_webp_received.split('/')[5]

        # Execute query to count data
        query = articles.count_documents({})
        category_num = query + 1
        # Execute query to fetch data
        articles.insert_one(
            {
                "slug": slug, "title": title, "body": body, "bodyUpdated": body_updated,
                "author": author,
                "datePosted": dt.now(), "dateUpdated": dt.now(), "likes": 0, "comments": [],
                "category": category, "category_num": category_num, "readTime": read_time,
                "id_jpg_cover": jpg_image_id, "id_webp_cover": webp_image_id,
                "imageAltText": image_alt_text, "status": status,
                "keywords": keywords
            }
        )

        flash(f"Blog posted {emojize(':grinning_face_with_big_eyes:')}", 'success')
        return redirect(url_for('dashboard'))


# View for edit article
class EditArticleEndpoint(MethodView):
    @staticmethod
    # @requires_auth
    def get(blog_id):
        # Create Mongodb connection
        articles = mongo.get_collection(name='articles')
        # Execute query to fetch only one data
        query = articles.find_one({"_id": ObjectId(blog_id)})
        # Get form
        form = ArticleForm(request.form)
        # populate form fields
        form.title.data = str(query["title"]).upper()
        form.keywords.data = str(query["keywords"])
        form.body.data = str(query["body"])
        form.category.data = str(query["category"])
        form.readTime.data = str(query["readTime"])
        form.status.data = str(query["status"])

        return render_template('edit_article.html', others=False, form=form)

    @staticmethod
    # @requires_auth
    def post(blog_id):
        # Create Mongodb connection
        articles = mongo.get_collection(name='articles')

        # Receive inputs sent through forms
        title = str(request.form['title']).upper()
        keywords = str(request.form['keywords'])
        body = str(request.form['body'])
        body_updated = True if request.form.get('bodyUpdated', 'off', type=str) == 'on' else False
        category = str(request.form['category'])
        read_time = str(request.form['readTime'])
        status = str(request.form['status'])
        date_updated = dt.now()

        # Execute query to find and update data
        articles.find_one_and_update(
            {'_id': ObjectId(blog_id)},
            {
                '$set': {
                    'title': title,
                    'body': body,
                    'bodyUpdated': body_updated,
                    'category': category,
                    'readTime': read_time,
                    'dateUpdated': date_updated,
                    'status': status,
                    'keywords': keywords
                }
            },
            upsert=False,
        )
        flash(f"Article Updated {emojize(':grinning_face_with_big_eyes:')}", 'success')
        return redirect(url_for('dashboard'))


# View for deleting article
class DeleteArticleEndpoint(MethodView):
    @staticmethod
    # @requires_auth
    def post(blog_id):
        # Create Mongodb connection
        articles = mongo.get_collection(name='articles')
        blog_id = str(blog_id)
        # Execute query to find and delete data
        articles.find_one_and_delete({"_id": ObjectId(blog_id)})
        flash(f"Article Deleted {emojize(':grinning_face_with_big_eyes:')}", 'success')

        return redirect(url_for('dashboard'))


# View for comment status
class CommentStatusEndpoint(MethodView):
    @staticmethod
    # @requires_auth
    def get():
        # Create Mongodb connection
        articles = mongo.get_collection(name='articles')
        # Execute query to fetch data from an array where value for the approved field is false and
        # it is sorted in a descending order based the date posted
        query = articles.find({
            "comments": {'$elemMatch': {'approved': False}}
        }).sort("{'comments': { '$elemMatch': 'datePosted'}}", DESCENDING)
        results = [item for item in query]
        return render_template('comments.html', results=results)


# View for comment approval
class CommentApprovalEndpoint(MethodView):
    @staticmethod
    # @requires_auth
    def get():
        # The clients send json data to the comment approval endpoint asynchronously using jquery, then
        # we receive the data and then reply the client with a json data
        # which is rendered in the template file using javascript
        ids = str(request.args.get('IDs', type=str))
        blog_id, comment_index, _ = ids.split('_')
        approved = str(request.args.get('approval', None, type=str))
        comment_id = str(request.args.get('commentID', None, type=str))
           
        if approved == 'true':
            # Create Mongodb connection
            articles = mongo.get_collection(name='articles')
            # Execute query to find and update data
            articles.find_one_and_update(
                {'_id': ObjectId(blog_id)},
                {
                    '$set': {f'comments.{comment_index}.approved': True}
                    },
                upsert=False,)     
            status = 200
            return {'status': status}   # dict object is transformed into a json object when received by client

        else:
            # Create Mongodb connection
            articles = mongo.get_collection(name='articles')
            # Execute query to find and update data
            articles.find_one_and_update(
                {'_id': ObjectId(blog_id)},
                { 
                    '$pull': {'comments': {'commentId': comment_id}}
                    },
                {'multi': True})
            status = 200
            return {'status': status}   # dict object is transformed into a json object when received by client


# View for registering new users
class RegisterUserEndpoint(MethodView):
    @staticmethod
    # @requires_auth
    def get():
        form = SignupForm(request.form)
        return render_template('register.html', others=False, form=form)

    @staticmethod
    # @requires_auth
    def post():
        # Create Mongodb connection
        users = mongo.get_collection(name='admin_user')

        # Get data entered by user
        last_name = str(request.form['last_name'])
        first_name = str(request.form['first_name'])
        user_email = str(request.form.get('email', None, type=str))     # Email is optional
        username = str(request.form['username'])
        gender = str(request.form['gender'])
        password = str(request.form['password'])
        bio = str(request.form['bio'])

        # Encrypt the raw password
        encrypted_password = bcrypt.generate_password_hash(str(password), rounds=10).decode('utf-8')

        # Insert data in mongo database
        users.insert_one({
            'lastName': last_name, 'firstName': first_name, 'password': encrypted_password,
            'biography': bio, 'email': user_email, 'username': username, 'gender': gender,
            'decryptedPasswd': password, 'dateCreated': dt.now(), 'dateModified': dt.now()
        })
        
        flash(f"New User Account Created {emojize(':grinning_face_with_big_eyes:')}", 'success')
        return redirect(url_for('dashboard'))


# ERROR PAGES
# 1.Error_404 Page
@app.errorhandler(404)
def error_404(error):
    return render_template('error.html', others=True), 404


# 2.Error_500 page
@app.errorhandler(500)
def error_500(error):
    return render_template('error.html', others=True), 500
