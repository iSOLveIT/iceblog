from flask.views import MethodView
from flask import render_template, redirect, request, url_for, flash, session
from content import mongo, app
from bson.objectid import ObjectId
from .form import ArticleForm, LoginForm
from datetime import datetime as dt
from passlib.hash import sha256_crypt
from functools import wraps
from flask_pymongo import pymongo
from emoji import emojize
from .user_views import logout_required


# Check if user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash(f"{emojize(':warning:')} Unauthorised access, Login first", 'danger')
            return redirect(url_for('admin')), 301
    return decorated_function


# View for admin login
class AdminLoginEndpoint(MethodView):
    @staticmethod
    @logout_required
    def get():
        form = LoginForm(request.form)
        return render_template('login.html', others=True, form=form), 200

    @staticmethod
    @logout_required
    def post():
        # Get data entered into Login form
        username = request.form['username']
        password = request.form['password']
        # Create Mongodb connection
        users = mongo.get_collection(name='admin_user')
        # Execute query to fetch data
        user = users.find_one({"username": username})
        # Authentication and Authorization
        if user is None:
            flash(f"{emojize(':warning:')} Invalid Login Credentials", 'danger')
            return redirect(url_for('admin'))
        if user:
            encrypted_password = user['password']
            if sha256_crypt.verify(password, encrypted_password):
                session['logged_in'] = True
                session['username'] = username
                session['lastName'] = user['lastName']
                session['firstName'] = user['firstName']
                session['gender'] = user['gender']

                users.find_one_and_update(
                    {'_id': ObjectId(user['_id'])},
                    {
                        '$set': {
                            'loginAt': dt.now()
                        }
                    },
                    upsert=False,
                )
                flash(f"Logged in successfully {emojize(':grinning_face_with_big_eyes:')}", 'success')
                return redirect(url_for('dashboard')), 301
            else:
                flash(f"{emojize(':warning:')} Password is incorrect", 'danger')
                return redirect(url_for('admin')), 301


# View for admin dashboard
class AdminEndpoint(MethodView):
    @staticmethod
    @login_required
    def get():
        # Get session username
        author = session.get('username')
        # Create Mongodb connection
        articles = mongo.get_collection(name='articles')
        # Execute query to fetch data
        posts = articles.find({"author": author}).sort('datePosted', pymongo.DESCENDING)
        return render_template('admin.html', others=False, posts=posts), 200


# View for admin logout
class AdminLogoutEndpoint(MethodView):
    @staticmethod
    @login_required
    def get():
        # Create Mongodb connection
        users = mongo.get_collection(name='admin_user')
        # Get session username
        username = session.get('username')
        # Execute query to fetch data
        users.find_one_and_update(
            {'username': username},
            {
                '$set': {
                    'logoutAt': dt.now()
                }
            },
            upsert=False,
        )
        session.clear()
        flash(f"Logged out {emojize(':grinning_face_with_big_eyes:')}", 'success')
        return redirect(url_for('admin')), 301


# View for admin account details
class AdminProfileEndpoint(MethodView):
    @staticmethod
    @login_required
    def get():
        # Create Mongodb connection
        users = mongo.get_collection(name='admin_user')
        # Get session username
        username = session.get('username')
        # Execute query to fetch data
        user_details = users.find_one({'username': username})
        return render_template('admin_profile.html', others=False, user=user_details), 200

    @staticmethod
    @login_required
    def post():
        lname = request.form['LName']
        fname = request.form['FName']
        email = request.form['Email']
        gender = request.form['Gender']
        password = request.form['password']
        
        _password = sha256_crypt.hash(str(password))  # Hash (encrypt) password
        # Create Mongodb connection
        users = mongo.get_collection(name='admin_user')
        # Get session username
        username = session.get('username')
        session['lastName'] = lname
        session['firstName'] = fname
        session['gender'] = gender
        session.modified = True
        users.find_one_and_update(
            {'username': username},
            {
                '$set': {
                    'lastName': lname, 'firstName': fname, 'password': _password,
                    'email': email, 'gender': gender, 'decrypted_pswd': password,
                    'dateModified': dt.now()
                }
            },
            upsert=False,
        )
        flash(f"Account details updated {emojize(':grinning_face_with_big_eyes:')}", 'success')
        return redirect(url_for('profile')), 301


# View for add article
class AddArticleEndpoint(MethodView):
    @staticmethod
    @login_required
    def get():
        form = ArticleForm(request.form)
        return render_template('add_article.html', others=False, form=form), 200

    @staticmethod
    @login_required
    def post():
        title = request.form['title']
        body = request.form['body']
        category = request.form['category']
        readTime = request.form['readTime']
        author = session.get('username')
        bodyUpdated = False

        # Create Mongodb connection
        articles = mongo.get_collection(name='articles')
        query = articles.count_documents({})
        category_num = query + 1
        # Execute query to fetch data
        articles.insert_one(
            {
                "title": title, "body": body, "bodyUpdated": bodyUpdated, "author": author,
                "datePosted": dt.now(), "dateUpdated": dt.now(), "likes": 0, "comments": [],
                "category": category, "category_num": category_num, "readTime": readTime
            }
        )

        flash(f"Blog posted {emojize(':grinning_face_with_big_eyes:')}", 'success')
        return redirect(url_for('dashboard')), 301


# View for edit article
class EditArticleEndpoint(MethodView):
    @staticmethod
    @login_required
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

        return render_template('edit_article.html', others=False, form=form), 200

    @staticmethod
    @login_required
    def post(blog_id):
        title = request.form['title']
        body = request.form['body']
        bodyUpdated = True if request.form.get('bodyUpdated', 'off', type=str) == 'on' else False
        category = request.form['category']
        readTime = request.form['readTime']
        dateUpdated = dt.now()
        # Create Mongodb connection
        articles = mongo.get_collection(name='articles')
        # Execute query to fetch data
        articles.find_one_and_update(
            {'_id': ObjectId(blog_id)},
            {
                '$set': {
                    'title': title,
                    'body': body,
                    'bodyUpdated': bodyUpdated,
                    'category': category,
                    'readTime': readTime,
                    'dateUpdated': dateUpdated,
                }
            },
            upsert=False,
        )
        flash(f"Article Updated {emojize(':grinning_face_with_big_eyes:')}", 'success')
        return redirect(url_for('dashboard')), 301


# View for deleting article
class DeleteArticleEndpoint(MethodView):
    @staticmethod
    @login_required
    def post(blog_id):
        # Create Mongodb connection
        articles = mongo.get_collection(name='articles')
        # Execute query to fetch data
        articles.find_one_and_delete({"_id": ObjectId(blog_id)})
        flash(f"Article Deleted {emojize(':grinning_face_with_big_eyes:')}", 'success')

        return redirect(url_for('dashboard')), 301


# View for approving comments
class CommentStatusEndpoint(MethodView):
    @staticmethod
    @login_required
    def get():
        # Create Mongodb connection
        articles = mongo.get_collection(name='articles')
        # Execute query to fetch data
        query = articles.find({
            "comments": {'$elemMatch': {'approved': False}}
        }).sort("{'comments': { '$elemMatch': 'datePosted'}}", pymongo.DESCENDING)
        results = [item for item in query]
        return render_template('comments.html', results=results), 200


class CommentApprovalEndpoint(MethodView):
    @staticmethod
    @login_required
    def get():
        ids = request.args.get('IDs', type=str)
        blog_id, commentIndex, _ = ids.split('_')
        approved = request.args.get('approval', None, type=str)
        comment_id = request.args.get('commentID', None, type=str)
           
        if approved == 'true':
            # Create Mongodb connection
            articles = mongo.get_collection(name='articles')
            # Execute query
            articles.find_one_and_update(
                {'_id': ObjectId(blog_id)},
                {
                    '$set': {f'comments.{commentIndex}.approved': True}
                    },
                upsert=False,)     
            status = 200
            return {'status': status}, 200

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
            return {'status': status}, 200


# ERROR PAGES
# 1.Error_404 Page
@app.errorhandler(404)
def error_404(error):
    return render_template('error.html', others=True), 404


# 2.Error_500 page
@app.errorhandler(500)
def error_500(error):
    return render_template('error.html', others=True), 500
