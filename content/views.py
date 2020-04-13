from flask.views import MethodView
from flask import render_template, session
from content import mongo
from bson.objectid import ObjectId      # Import for using mongo id
from flask_pymongo import pymongo


# View for index
class IndexEndpoint(MethodView):
    @staticmethod
    def get():
        # session['logged_in'] = True
        # Create Mongodb connection
        articles = mongo.db.articles

        # Execute query to fetch data
        random_posts = articles.find({"likes": {'$gte': 12}}).limit(5)

        # Loop through random_posts and store as a list
        random_post = [item for item in random_posts]

        # Execute query to fetch data
        recent_posts = articles.find().limit(6)
        return render_template('index.html', random_post=random_post,
                               recent_posts=recent_posts), 200


# View for about
class AboutEndpoint(MethodView):
    @staticmethod
    def get():
        return render_template('about.html'), 200


# View for contact
class ContactEndpoint(MethodView):
    @staticmethod
    def get():
        return render_template('contact.html'), 200


# View for blog category
class CategoryEndpoint(MethodView):
    @staticmethod
    def get(category):
        # Create Mongodb connection
        articles = mongo.db.articles

        # Execute query to fetch data
        posts = articles.find({"category": category})

        return render_template('category.html', posts=posts,
                               category=category), 200


# View for single blog
class SingleEndpoint(MethodView):
    @staticmethod
    def get(category, blog_id):
        # Create Mongodb connection
        articles = mongo.db.articles

        # Execute query to fetch data
        article = articles.find_one({"_id": ObjectId(blog_id)})

        # Execute query to fetch data
        popular_posts = articles.find({"likes": {'$gt': 12}}).limit(3)

        # Number of comments
        len_comments = len(article['comments'])

        # Execute query to fetch data
        related_posts = articles.find({"likes": {'$gte': 10}}).limit(4).sort('datePosted',
                                                      pymongo.DESCENDING)

        related_post = [item for item in related_posts]

        # color codes for category
        category_color = {
            "Lifestyle": "primary",
            "Tech": "danger",
            "Sports": "info",
            "Entertainment": "warning",
            "Health": "success"
        }

        cat_color = [category_color[item['category']] for item in related_post if item['category'] in category_color]
        return render_template('single.html', article=article,
                               len_comments=len_comments,
                               popular_posts=popular_posts,
                               related_post=related_post,
                               cat_color=cat_color), 200
