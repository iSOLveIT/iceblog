from flask.views import MethodView
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from content import mongo
from bson.objectid import ObjectId  # Import for using mongo id
from flask_pymongo import pymongo
from .form import CommentForm
from datetime import datetime as dt
from functools import wraps
from emoji import emojize


# Check if admin is logged out
def logout_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            flash(f"{emojize(':warning:')} Unauthorised access, Logout first", 'danger')
            return redirect(url_for('dashboard'))
        else:
            return f(*args, **kwargs)
    return decorated_function


# View for index
class IndexEndpoint(MethodView):
    @staticmethod
    @logout_required
    def get():
        # Create Mongodb connection
        articles = mongo.db.articles

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
            "Sports": "info",
            "Entertainment": "warning",
            "Health": "success"
        }
        return render_template('index.html', random_post=random_post,
                               recent_posts=recent_posts, catColor=category_color
                               ), 200

    @staticmethod
    @logout_required
    def post():
        e_mail = request.form['newsletter']
        dB = mongo.db.newsletter_subscribers
        dB.insert_one({"emailAddress": e_mail, "dateCreated": dt.now()})
        flash(f"Email received {emojize(':grinning_face_with_big_eyes:')}", 'success')
        return redirect(url_for('index', _anchor='newsletter'))


# View for about
class AboutEndpoint(MethodView):
    @staticmethod
    @logout_required
    def get():
        return render_template('about.html'), 200


# View for contact
class ContactEndpoint(MethodView):
    @staticmethod
    @logout_required
    def get():
        return render_template('contact.html'), 200


# View for blog category
class CategoryEndpoint(MethodView):
    @staticmethod
    @logout_required
    def get(category):
        offset = int(request.args['page'])
        limit = 6
        # Create Mongodb connection
        articles = mongo.db.articles
        _total_doc = articles.count_documents({'category': category})
        if offset < 0 or offset >= int(_total_doc):
            return redirect(url_for('category', category=category, page=0))
        else:
            # Execute query to fetch data
            posts = articles.find({'$and': [
                {"category": category},
                {"category_num": {'$gte': offset}}
            ]}).limit(limit).sort('category_num', pymongo.ASCENDING)

            _previous = int(offset) - limit
            _next = int(offset) + limit

            # color codes for category
            category_info = {
                "Lifestyle": ["primary", "This is a description for Lifestyle"],
                "Tech": ["danger", "This is a description for Tech"],
                "Sports": ["info", "This is a description for Sports"],
                "Entertainment": ["warning", "This is a description for Entertainment"],
                "Health": ["success", "This is a description for Health"]
            }

            # select category color
            cat_info = []
            if category in category_info:
                cat_info = category_info.get(category)

        return render_template('category.html', posts=posts,
                               _previous=_previous, _next=_next,
                               category=category, cat_info=cat_info), 200


# View for single blog
class SingleEndpoint(MethodView):
    @staticmethod
    @logout_required
    def get(category, blog_id):
        # Create Mongodb connection
        articles = mongo.db.articles

        # Execute query to fetch data
        article = articles.find_one({"_id": ObjectId(blog_id)})

        # Execute query to fetch data
        popular_posts = articles.find({"likes": {'$gt': 12}}).limit(5).sort('datePosted', pymongo.DESCENDING)

        # Number of comments
        len_comments = len(article['comments'])

        # Execute query to fetch data
        related_posts = [d for d in articles.aggregate([{'$sample': {'size': 4}}])]

        related_post = [item for item in related_posts]

        # color codes for category
        category_color = {
            "Lifestyle": "primary",
            "Tech": "danger",
            "Sports": "info",
            "Entertainment": "warning",
            "Health": "success"
        }
        # Color for category
        article_color = category_color.get(category)
        cat_color = [category_color[item['category']] for item in related_post if item['category'] in category_color]

        # Comment form
        form = CommentForm()

        # Numbers of articles for each category
        lifestyle = articles.count_documents({"category": "Lifestyle"})
        tech = articles.count_documents({"category": "Tech"})
        sports = articles.count_documents({"category": "Sports"})
        entertain = articles.count_documents({"category": "Entertainment"})
        health = articles.count_documents({"category": "Health"})
        len_category = [lifestyle, health, entertain, tech, sports]

        return render_template('single.html', article=article,
                               len_comments=len_comments, form=form,
                               popular_posts=popular_posts,
                               related_post=related_post,
                               cat_color=cat_color, len_category=len_category,
                               article_color=article_color), 200

    @staticmethod
    @logout_required
    def post(category, blog_id):
        if 'name' and 'msg' in request.form:
            name = request.form['name']
            message = request.form['msg']
            datePosted = dt.now()
            # Create Mongodb connection
            dB = mongo.db.articles

            # Execute query to fetch data
            dB.find_one_and_update(
                {"_id": ObjectId(blog_id)},
                {
                    "$push": {
                        "comments": {
                            "name": name,
                            "datePosted": datePosted,
                            "message": message
                        }
                    }
                }
            )
            return redirect(url_for('blogpost', category=category,
                                    blog_id=blog_id, _anchor='comment-section'))

        elif 'newsletter' in request.form:
            e_mail = request.form['newsletter']
            dB = mongo.db.newsletter_subscribers
            dB.insert_one({"emailAddress": e_mail, "dateCreated": dt.now()})
            flash(f"Email received {emojize(':grinning_face_with_big_eyes:')}", 'success')
            return redirect(url_for('blogpost', category=category,
                                    blog_id=blog_id, _anchor='newsletter'))


# View for likes
class LikesEndpoint(MethodView):
    @staticmethod
    @logout_required
    def get():
        blog_id = request.args.get('blog_id', type=str)
        likes = request.args.get('no_likes', 0, type=int)
        likes = int(likes)

        # Create Mongodb connection
        articles = mongo.db.articles
        articles.find_one_and_update(
            {'_id': ObjectId(blog_id)},
            {'$inc': {'likes': likes}}
        )
        query = articles.find_one({'_id': ObjectId(blog_id)})
        result = query['likes']
        if likes == +1:
            return jsonify(result=result)
        else:
            return jsonify(result=result)
