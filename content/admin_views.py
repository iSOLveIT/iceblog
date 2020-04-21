from flask.views import MethodView
from flask import render_template, redirect, request, url_for, flash, session
from content import mongo
from bson.objectid import ObjectId
from .form import ArticleForm, LoginForm
from datetime import datetime as dt
from passlib.hash import sha256_crypt
from functools import wraps
from flask_pymongo import pymongo


# Check if user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorised access, Login first.', 'danger')
            return redirect(url_for('admin'))
    return decorated_function


# View for admin login
class AdminLoginEndpoint(MethodView):
    @staticmethod
    def get():
        form = LoginForm(request.form)
        return render_template('login.html', form=form), 200

    @staticmethod
    def post():
        # Get data entered into Login form
        username = request.form['username']
        password = request.form['password']

        # Create Mongodb connection
        users = mongo.db.admin_user

        # Execute query to fetch data
        user = users.find_one({"username": username})

        # Authentication and Authorization
        if user is None:
            flash('Invalid Login Credentials :(', 'danger')
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
                flash('Logged in successfully.', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Password is incorrect !', 'danger')
                return redirect(url_for('admin'))


# View for admin logout
class AdminLogoutEndpoint(MethodView):
    @staticmethod
    @login_required
    def get():
        # Create Mongodb connection
        users = mongo.db.admin_user

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
        flash('Logged out.', 'success')
        return redirect(url_for('admin'))


# View for admin dashboard
class AdminEndpoint(MethodView):
    @staticmethod
    @login_required
    def get():
        # Get session first name and last name
        fName = session.get('firstName')
        lName = session.get('lastName')
        author = fName + ' ' + lName
        # Create Mongodb connection
        articles = mongo.db.articles

        # Execute query to fetch data
        posts = articles.find({"author": author}).sort('datePosted', pymongo.DESCENDING)
        return render_template('admin.html', posts=posts), 200


# View for add article
class AddArticleEndpoint(MethodView):
    @staticmethod
    @login_required
    def get():
        form = ArticleForm(request.form)
        return render_template('add_article.html', form=form), 200

    @staticmethod
    @login_required
    def post():
        title = request.form['title']
        body = request.form['body']
        link = request.form['link']
        category = request.form['category']
        readTime = request.form['readTime']
        author = session.get('firstName') + " " + session.get('lastName')

        # Create Mongodb connection
        articles = mongo.db.articles

        # Execute query to fetch data
        articles.insert_one(
            {
                "title": title, "body": body, "coverimageLink": link, "author": author,
                "datePosted": dt.now(), "dateUpdated": dt.now(), "likes": 0,
                "comments": [], "category": category, "readTime": readTime
            }
        )

        flash('Blog posted succesfully.', 'success')
        return redirect(url_for('dashboard'))


# View for edit article
class EditArticleEndpoint(MethodView):
    @staticmethod
    @login_required
    def get(blog_id):
        # Create Mongodb connection
        articles = mongo.db.articles

        # Execute query to fetch data
        query = articles.find_one({"_id": ObjectId(blog_id)})

        # GEt form
        form = ArticleForm(request.form)

        # populate form fields
        form.title.data = query["title"]
        form.body.data = query["body"]
        form.link.data = query["coverimageLink"]
        form.category.data = query["category"]
        form.readTime.data = query["readTime"]

        return render_template('edit_article.html', form=form), 200

    @staticmethod
    @login_required
    def post(blog_id):
        title = request.form['title']
        body = request.form['body']
        link = request.form['link']
        category = request.form['category']
        readTime = request.form['readTime']
        dateUpdated = dt.now()

        # Create Mongodb connection
        articles = mongo.db.articles

        # Execute query to fetch data
        articles.find_one_and_update(
            {'_id': ObjectId(blog_id)},
            {
                '$set': {
                    'title': title,
                    'body': body,
                    'coverimageLink': link,
                    'category': category,
                    'readTime': readTime,
                    'dateUpdated': dateUpdated,
                }
            },
            upsert=False,
        )
        flash('Article Updated.', 'success')
        return redirect(url_for('dashboard'))


# View for deleting article
class DeleteArticleEndpoint(MethodView):
    @staticmethod
    @login_required
    def post(blog_id):
        # Create Mongodb connection
        articles = mongo.db.articles

        # Execute query to fetch data
        articles.find_one_and_delete({"_id": ObjectId(blog_id)})
        flash('Article Deleted.', 'success')

        return redirect(url_for('dashboard'))
