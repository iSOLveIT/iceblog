from flask.views import MethodView
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from content import mongo
from bson.objectid import ObjectId  # Import for using mongo id
from flask_pymongo import pymongo
from .form import CommentForm
from datetime import datetime as dt
from functools import wraps
from emoji import emojize
from .commentIDgenerator import random_string


# Check if admin is logged out
def logout_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            flash(f"{emojize(':warning:')} Unauthorised access, Logout first", 'danger')
            return redirect(url_for('dashboard')), 301
        else:
            return f(*args, **kwargs)

    return decorated_function


# View for index
class IndexEndpoint(MethodView):
    @staticmethod
    @logout_required
    def get():
        # Create Mongodb connection
        articles = mongo.get_collection(name='articles')
        # Execute query to fetch data
        random_posts = [d for d in articles.aggregate([{'$sample': {'size': 5}}])]
        # Loop through random_posts and store as a list
        random_post = [item for item in random_posts]
        # Execute query to fetch data
        recent_posts = articles.find(
            {
                "datePosted": {
                    "$gt": dt.strptime('2019,12,31', '%Y,%m,%d')
                }
            }
        ).limit(6)

        # color codes for category
        category_color = {
            "Lifestyle": "primary",
            "Tech": "danger",
            "Education": "info",
            "Entertainment": "warning",
            "Health": "success"
        }
        return render_template('index.html', random_post=random_post, others=False,
                               recent_posts=recent_posts, catColor=category_color
                               ), 200

    @staticmethod
    @logout_required
    def post():
        e_mail = request.form['newsletter']
        dB = mongo.get_collection(name='newsletter_subscribers')
        dB.insert_one({"emailAddress": e_mail, "dateCreated": dt.now()})
        flash(f"Email received {emojize(':grinning_face_with_big_eyes:')}", 'success')
        return redirect(url_for('index', _anchor='newsletter')), 301


# View for about
class AboutEndpoint(MethodView):
    @staticmethod
    @logout_required
    def get():
        return render_template('about.html', others=False), 200


# View for contact
class ContactEndpoint(MethodView):
    @staticmethod
    @logout_required
    def get():
        return render_template('contact.html', others=False), 200


# View for blog category
class CategoryEndpoint(MethodView):
    @staticmethod
    @logout_required
    def get():
        offset = int(request.args['page'])
        limit = 12
        # Create Mongodb connection
        articles = mongo.get_collection(name='articles')
        _total_doc = articles.count_documents({})
        if offset < 0 or offset >= int(_total_doc):
            return redirect(url_for('category', page=0)), 301
        else:
            # Execute query to fetch data
            posts = articles.find(
                {"category_num": {'$gte': offset}}
            ).limit(limit).sort('category_num', pymongo.ASCENDING)

            _previous = int(offset) - limit
            _next = int(offset) + limit

            # color codes for category
            category_color = {
                "Lifestyle": "primary",
                "Tech": "danger",
                "Education": "info",
                "Entertainment": "warning",
                "Health": "success"
            }

            # # select category color
            # cat_info = []
            # if category in category_info:
            #     cat_info = category_info.get(category)

        return render_template('category.html', posts=posts,
                               _previous=_previous, _next=_next,
                               others=False, color=category_color), 200


# View for single blog
class SingleEndpoint(MethodView):
    @staticmethod
    @logout_required
    def get(blog_id):
        # Create Mongodb connection
        articles = mongo.get_collection(name='articles')
        # Execute query to fetch data
        article = articles.find_one({"_id": ObjectId(blog_id)})
        # Execute query to fetch data
        popular_posts = articles.find({"likes": {'$gt': 16}}).limit(5).sort('datePosted', pymongo.DESCENDING)
        # Number of comments
        len_comments = len([comment for comment in article['comments'] if comment['approved'] == True])
        # Execute query to fetch data
        related_posts = [d for d in articles.aggregate([{'$sample': {'size': 4}}])]
        related_post = [item for item in related_posts]
        # color codes for category
        category_color = {
            "Lifestyle": "primary",
            "Tech": "danger",
            "Education": "info",
            "Entertainment": "warning",
            "Health": "success"
        }
        # Comment form
        form = CommentForm()

        return render_template('single.html', article=article,
                               len_comments=len_comments, form=form,
                               popular_posts=popular_posts,
                               related_post=related_post,
                               others=False, color=category_color), 200

    @staticmethod
    @logout_required
    def post(blog_id):
        if 'name' and 'msg' in request.form:
            name = request.form['name']
            message = request.form['msg']
            datePosted = dt.now()
            approval = False
            comment_id = random_string()
            # Create Mongodb connection
            articles = mongo.get_collection(name='articles')
            # Execute query to fetch data
            articles.find_one_and_update(
                {"_id": ObjectId(blog_id)},
                {
                    "$push": {
                        "comments": {
                            "name": name,
                            "datePosted": datePosted,
                            "message": message,
                            "approved": approval,
                            "commentId": comment_id
                        }
                    }
                }
            )
            return redirect(url_for('blogpost', blog_id=blog_id, _anchor='comment-section')), 301

        elif 'newsletter' in request.form:
            e_mail = request.form['newsletter']
            dB = mongo.get_collection(name='newsletter_subscribers')
            dB.insert_one({"emailAddress": e_mail, "dateCreated": dt.now()})
            flash(f"Email received {emojize(':grinning_face_with_big_eyes:')}", 'success')
            return redirect(url_for('blogpost', blog_id=blog_id, _anchor='newsletter')), 301


# View for likes
class LikesEndpoint(MethodView):
    @staticmethod
    @logout_required
    def get():
        blog_id = request.args.get('blog_id', type=str)
        likes = request.args.get('no_likes', 0, type=int)
        likes = int(likes)

        # Create Mongodb connection
        articles = mongo.get_collection(name='articles')
        articles.find_one_and_update(
            {'_id': ObjectId(blog_id)},
            {'$inc': {'likes': likes}}
        )
        query = articles.find_one({'_id': ObjectId(blog_id)})
        result = query['likes']
        if likes == +1:
            return jsonify(result=result), 200
        else:
            return jsonify(result=result), 200
