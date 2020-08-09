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
            'username': user_info['nickname'],
            'firstName': user_info['name'].split(' ')[0],
            'lastName': user_info['name'].split(' ')[1],
            'gender': user_info['gender'],
            'picture': user_info['picture']
        }
        
        flash(f"Logged in successfully {emojize(':grinning_face_with_big_eyes:')}", 'success')
        return redirect(url_for('dashboard'))
            

# View for admin dashboard
class AdminDashboardEndpoint(MethodView):
    @staticmethod
    @requires_auth
    def get():
        # Get user information stored in session
        user_info = session.get(PROFILE_KEY)

        # Get username from user info
        author = user_info['username']

        # Create Mongodb connection
        articles = mongo.get_collection(name='articles')

        # Execute query to fetch data from database
        posts = articles.find({"author": author}).sort('datePosted', DESCENDING)
        return render_template('admin.html', others=False, posts=posts, user_info=user_info)


# View for admin logout
class AdminLogoutEndpoint(MethodView):
    @staticmethod
    @requires_auth
    def get():
        session.clear()     # Clear all data in session
        params = {'returnTo': url_for('index', _external=True), 'client_id': AUTH0_CLIENT_ID}
        # Logout user and redirect user to homepage
        return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))
        

# View for admin account details
class AdminProfileEndpoint(MethodView):
    @staticmethod
    @requires_auth
    def get():
        # Create Mongodb connection
        users = mongo.get_collection(name='admin_user')
        # Get user information stored in session and get only username
        username = session.get(PROFILE_KEY)['username']
        # Execute query to fetch data
        user_details = users.find_one({'username': username})
        return render_template('admin_profile.html', others=False, user=user_details)

    @staticmethod
    @requires_auth
    def post():
        last_name = str(request.form['LName'])
        first_name = str(request.form['FName'])
        email = str(request.form['Email'])
        gender = str(request.form['Gender'])
        password = str(request.form['password'])
        
        _password = bcrypt.generate_password_hash(str(password), rounds=10).decode('utf-8')  # Hash (encrypt) password
        # Create Mongodb connection
        users = mongo.get_collection(name='admin_user')
        # Get user information stored in session and get only username
        username = session.get(PROFILE_KEY)['username']
        session[PROFILE_KEY]['lastName'] = last_name
        session[PROFILE_KEY]['firstName'] = first_name
        session[PROFILE_KEY]['gender'] = gender
        session.modified = True
        users.find_one_and_update(
            {'username': username},
            {
                '$set': {
                    'lastName': last_name, 'firstName': first_name, 'password': _password,
                    'email': email, 'gender': gender, 'decryptedPasswd': password,
                    'dateModified': dt.now()
                }
            },
            upsert=False,
        )
        flash(f"Account details updated {emojize(':grinning_face_with_big_eyes:')}", 'success')
        return redirect(url_for('profile'))


# View for add article
class AddArticleEndpoint(MethodView):
    @staticmethod
    @requires_auth
    def get():
        form = ArticleForm(request.form)
        return render_template('add_article.html', others=False, form=form)

    @staticmethod
    @requires_auth
    def post():
        title = str(request.form['title'])
        body = str(request.form['body'])
        category = str(request.form['category'])
        read_time = str(request.form['readTime'])
        author = str(session.get(PROFILE_KEY)['username'])   # Get user info stored in session and get only username
        body_updated = False

        # Create Mongodb connection
        articles = mongo.get_collection(name='articles')
        query = articles.count_documents({})
        category_num = query + 1
        # Execute query to fetch data
        articles.insert_one(
            {
                "title": title, "body": body, "bodyUpdated": body_updated, "author": author,
                "datePosted": dt.now(), "dateUpdated": dt.now(), "likes": 0, "comments": [],
                "category": category, "category_num": category_num, "readTime": read_time
            }
        )

        flash(f"Blog posted {emojize(':grinning_face_with_big_eyes:')}", 'success')
        return redirect(url_for('dashboard'))


# View for edit article
class EditArticleEndpoint(MethodView):
    @staticmethod
    @requires_auth
    def get(blog_id):
        # Create Mongodb connection
        articles = mongo.get_collection(name='articles')
        # Execute query to fetch data
        query = articles.find_one({"_id": ObjectId(blog_id)})
        # Get form
        form = ArticleForm(request.form)
        # populate form fields
        form.title.data = query["title"]
        form.body.data = query["body"]
        form.category.data = query["category"]
        form.readTime.data = query["readTime"]

        return render_template('edit_article.html', others=False, form=form)

    @staticmethod
    @requires_auth
    def post(blog_id):
        title = str(request.form['title'])
        body = str(request.form['body'])
        body_updated = True if request.form.get('bodyUpdated', 'off', type=str) == 'on' else False
        category = str(request.form['category'])
        read_time = str(request.form['readTime'])
        date_updated = dt.now()
        # Create Mongodb connection
        articles = mongo.get_collection(name='articles')
        # Execute query to fetch data
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
                }
            },
            upsert=False,
        )
        flash(f"Article Updated {emojize(':grinning_face_with_big_eyes:')}", 'success')
        return redirect(url_for('dashboard'))


# View for deleting article
class DeleteArticleEndpoint(MethodView):
    @staticmethod
    @requires_auth
    def post(blog_id):
        # Create Mongodb connection
        articles = mongo.get_collection(name='articles')
        # Execute query to fetch data
        articles.find_one_and_delete({"_id": ObjectId(blog_id)})
        flash(f"Article Deleted {emojize(':grinning_face_with_big_eyes:')}", 'success')

        return redirect(url_for('dashboard'))


# View for comment status
class CommentStatusEndpoint(MethodView):
    @staticmethod
    @requires_auth
    def get():
        # Create Mongodb connection
        articles = mongo.get_collection(name='articles')
        # Execute query to fetch data
        query = articles.find({
            "comments": {'$elemMatch': {'approved': False}}
        }).sort("{'comments': { '$elemMatch': 'datePosted'}}", DESCENDING)
        results = [item for item in query]
        return render_template('comments.html', results=results)


# View for comment approval
class CommentApprovalEndpoint(MethodView):
    @staticmethod
    @requires_auth
    def get():
        ids = request.args.get('IDs', type=str)
        blog_id, comment_index, _ = ids.split('_')
        approved = request.args.get('approval', None, type=str)
        comment_id = request.args.get('commentID', None, type=str)
           
        if approved == 'true':
            # Create Mongodb connection
            articles = mongo.get_collection(name='articles')
            # Execute query
            articles.find_one_and_update(
                {'_id': ObjectId(blog_id)},
                {
                    '$set': {f'comments.{comment_index}.approved': True}
                    },
                upsert=False,)     
            status = 200
            return {'status': status}

        else:
            # Create Mongodb connection
            articles = mongo.get_collection(name='articles')
            # Execute query
            articles.find_one_and_update(
                {'_id': ObjectId(blog_id)},
                { 
                    '$pull': {'comments': {'commentId': comment_id}}
                    },
                {'multi': True})
            status = 200
            return {'status': status}


# View for registering new users
class RegisterUserEndpoint(MethodView):
    @staticmethod
    @requires_auth
    def get():
        form = SignupForm(request.form)
        return render_template('register.html', others=False, form=form)

    @staticmethod
    @requires_auth
    def post():
        # Get data entered by user
        last_name = str(request.form['last_name'])
        first_name = str(request.form['first_name'])
        user_email = str(request.form.get('email', None, type=str))
        username = str(request.form['username'])
        gender = str(request.form['gender'])
        password = str(request.form['password'])
        bio = str(request.form['bio'])
        
        salted_password = bcrypt.generate_password_hash(str(password), rounds=10).decode('utf-8')

        # Create Mongodb connection
        users = mongo.get_collection(name='admin_user')
        # Insert data in mongo database
        users.insert_one({
            'lastName': last_name, 'firstName': first_name, 'password': salted_password,
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
