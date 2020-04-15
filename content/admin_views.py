from flask.views import MethodView
from flask import render_template, redirect, request, url_for, flash, session
from content import mongo
from bson.objectid import ObjectId
from .form import ArticleForm
from datetime import datetime as dt


# View for admin dashboard
class AdminEndpoint(MethodView):
    @staticmethod
    def get():
        # Create Mongodb connection
        articles = mongo.db.articles

        # Execute query to fetch data
        posts = articles.find()

        session['logged_in'] = True
        return render_template('admin.html', posts=posts), 200


# View for add article
class AddArticleEndpoint(MethodView):
    @staticmethod
    def get():
        form = ArticleForm()
        return render_template('add_article.html', form=form), 200

    @staticmethod
    def post():
        title = request.form['title']
        body = request.form['body']
        link = request.form['link']
        category = request.form['category']
        readTime = request.form['readTime']
        author = "Randy Duodu"

        # Create Mongodb connection
        articles = mongo.db.articles

        # Execute query to fetch data
        articles.insert_one(
            {
                "title": title, "body": body, "coverimageLink": link, "author": author,
                "datePosted": dt.now(), "dateUpdated": dt.now(), "likes": 0,
                "comments":[], "category": category, "readTime": readTime
            }
        )

        flash('Blog posted succesfully.', 'success')
        return redirect(url_for('dashboard'))


# View for edit article
class EditArticleEndpoint(MethodView):
    @staticmethod
    def get(blog_id):
        # Create Mongodb connection
        articles = mongo.db.articles

        # Execute query to fetch data
        query = articles.find_one({"_id": ObjectId(blog_id)})

        # GEt form
        form = ArticleForm()

        # populate form fields
        form.title.data = query["title"]
        form.body.data = query["body"]
        form.link.data = query["coverimageLink"]
        form.category.data = query["category"]
        form.readTime.data = query["readTime"]

        return render_template('edit_article.html', form=form), 200

    @staticmethod
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
    def post(blog_id):
        # Create Mongodb connection
        articles = mongo.db.articles

        # Execute query to fetch data
        articles.find_one_and_delete({"_id": ObjectId(blog_id)})
        flash('Article Deleted.', 'success')

        return redirect(url_for('dashboard'))
