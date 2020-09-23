# Local modules
from datetime import datetime as dt

# User-defined modules
from content import mongo
from .form import CommentForm
from .contact import send_email, reply_message
from .commentIDgenerator import comments_id

# Third-party modules
from flask.views import MethodView
from flask import render_template, request, redirect, url_for, flash
from bson.objectid import ObjectId  # Import for using mongo id
from pymongo import DESCENDING, ASCENDING
from emoji import emojize


# View for index
class IndexEndpoint(MethodView):
    @staticmethod
    def get():
        # Create Mongodb connection
        articles = mongo.get_collection(name='articles')
        quotes = mongo.get_collection(name='quotes')
        # Execute query to fetch 5 random data from the database
        random_posts = articles.aggregate([
            {'$match': {'status': "published"}},
            {'$sample': {'size': 5}},
            {'$project': {"_id": 0, "title": 1, "slug": 1, "datePosted": 1,
                          "category": 1, "id_jpg_cover": 1, "id_webp_cover": 1}}
        ])
        random_post = [item for item in random_posts]
        # Execute query to fetch 3 data which is sorted in a descending order
        recent_posts = articles.find(
            {"status": "published"},
            {"_id": 0, "bodyUpdated": 0, "dateUpdated": 0, "comments": 0, "likes": 0, "status": 0}
        ).limit(3).sort('datePosted', DESCENDING)
        # Execute query to fetch 1 random data from the database
        inspiration = [d for d in quotes.aggregate([{'$sample': {'size': 1}}])]

        return render_template('index.html', random_post=random_post, others=False,
                               recent_posts=recent_posts, inspire=inspiration,
                               year=dt.now().year)

    @staticmethod
    def post():
        # Create Mongodb connection
        # db = mongo.get_collection(name='newsletter_subscribers')
        # Receive the email entered by the user in the subscription section at the home page
        e_mail = str(request.form['newsletter'])
        # Execute query to insert data
        # db.insert_one({"emailAddress": e_mail, "dateCreated": dt.now()})
        flash(f"Thanks for subscribing {emojize(':grinning_face_with_big_eyes:')}", 'info')
        return redirect(url_for('index', _anchor='newsletter'))


# View for about
class AboutEndpoint(MethodView):
    @staticmethod
    def get():
        # Create Mongodb connection
        users = mongo.get_collection(name='admin_user')
        # Execute query to fetch all data but exclude some fields
        team = users.find({}, {
            "password": 0, "decryptedPasswd": 0,
            "dateCreated": 0, "dateModified": 0,
            "gender": 0, "_id": 0
        })  # Return collection but excludes the fields stated above
        # 0 = exclude specified field and 1 = include specified field

        return render_template('about.html', others=False, team=team, year=dt.now().year)


# View for contact
class ContactEndpoint(MethodView):
    @staticmethod
    def get():
        return render_template('contact.html', others=False, year=dt.now().year)

    @staticmethod
    def post():
        # Receive data inputs from contact form
        full_name = str(request.form.get('user_full_name', None, type=str))
        email = str(request.form.get('user_email', None, type=str))
        subject = str(request.form.get('user_subject', None, type=str))
        message = str(request.form.get('message', None, type=str))

        # Send message to IceBlog team
        send_email(_name=full_name, _subject=subject, _email=email, _body=message)
        # Reply user with message received from IceBlog team
        reply_message(_email=email, _sender=full_name)
        # Send a notification on the contact page for the user
        flash(f"Your message has been received {emojize(':grinning_face_with_big_eyes:')}", 'info')
        return redirect(url_for('contact', _anchor='flash'))


# View for blog category
class CategoryEndpoint(MethodView):
    @staticmethod
    def get():
        offset = int(request.args['page'])
        limit = 6
        # Create Mongodb connection
        articles = mongo.get_collection(name='articles')
        # Execute query to count data
        _total_doc = articles.count_documents({"status": "published"})
        if offset < 0 or offset >= int(_total_doc):
            return redirect(url_for('category', page=0))
        else:
            # Execute query to fetch limited data which is sorted in a ascending order
            posts = articles.find(
                {"$and": [{"category_num": {'$gt': offset}}, {"status": "published"}]},
                {"_id": 0, "bodyUpdated": 0, "dateUpdated": 0, "comments": 0, "likes": 0, "status": 0}
            ).limit(limit).sort('category_num', ASCENDING)

            _previous = int(offset) - limit
            _next = int(offset) + limit

        return render_template('category.html', posts=posts, year=dt.now().year,
                               _previous=_previous, _next=_next,
                               others=False)


# View for single blog
class SingleEndpoint(MethodView):
    @staticmethod
    def get(blog_category, blog_title, slug):
        # Create Mongodb connection
        articles = mongo.get_collection(name='articles')
        quotes = mongo.get_collection(name='quotes')
        # Execute query to fetch only 1 data
        topic = str(blog_title).upper().replace('_', ' ')
        get_id = articles.find_one({"slug": slug}, {"_id": 1})
        article = articles.find_one({
            "$and": [{"_id": ObjectId(get_id["_id"])}, {"title": topic}],
            },
            {"_id": 0, "category_num": 0}
        )
        # Number of comments
        len_comments = len([comment for comment in article['comments'] if comment['approved'] is True])
        # Execute query to fetch 4 random data from the database
        related_post = [d for d in articles.aggregate(
            [
                {'$match': {'status': "published"}},
                {'$sample': {'size': 4}},
                {'$project': {"_id": 0, "title": 1, "slug": 1, "datePosted": 1,
                              "category": 1, "id_jpg_cover": 1, "id_webp_cover": 1}}
            ]
        )]
        # Execute query to fetch 1 random data from the database
        inspiration = [d for d in quotes.aggregate([{'$sample': {'size': 1}}])]
        # Comment form
        form = CommentForm()

        return render_template('single.html', article=article, year=dt.now().year,
                               len_comments=len_comments, form=form,
                               related_post=related_post, inspire=inspiration,
                               others=False, category=blog_category)

    @staticmethod
    def post(blog_category, blog_title, slug):
        # Create Mongodb connection
        articles = mongo.get_collection(name='articles')
        # db = mongo.get_collection(name='newsletter_subscribers')

        topic = str(blog_title).upper().replace('_', ' ')
        blog_id = articles.find_one({"slug": slug}, {"_id": 1})

        # On a single blog post page, we have the comment form and the subscription form.
        # The client makes a post requests to the single blog endpoint asynchronously using jquery.

        # In order to differentiate which form data we are receiving, we check with an if-else
        # clause to identify if the form data sent has a certain input or not.

        # We receive the data and then reply the client with a json data
        # which is rendered in the template file using javascript
        if 'comment_name' and 'comment_msg' in request.form:
            comment_name = str(request.form['comment_name']).title()
            comment_msg_received = str(request.form['comment_msg']).split('. ')
            comment_msg = '. '.join([i.capitalize() for i in comment_msg_received])
            date_posted = dt.now()
            approval = False
            comment_id = comments_id()

            # Execute query to update data
            articles.find_one_and_update(
                {"$and": [{"_id": ObjectId(blog_id["_id"])}, {"title": topic}]},
                {
                    "$push": {
                        "comments": {
                            "name": comment_name,
                            "datePosted": date_posted,
                            "message": comment_msg,
                            "approved": approval,
                            "commentId": comment_id
                        }
                    }
                }
            )
            alert = f"Comment received. The team will review before publishing {emojize(':grinning_face_with_big_eyes:')}"
            return {"result": alert}

        elif 'subscriber_email' in request.form:
            e_mail = str(request.form['subscriber_email'])
            # Execute query to insert data
            # db.insert_one({"emailAddress": e_mail, "dateCreated": dt.now()})
            alert = f"Thanks for subscribing {emojize(':grinning_face_with_big_eyes:')}"
            return {"result": alert}
        else:
            return redirect(url_for('blog_category', blog_category=blog_category,
                                    blog_title=blog_title, slug=slug))


# View for likes
class LikesEndpoint(MethodView):
    @staticmethod
    def post():
        # Create Mongodb connection
        articles = mongo.get_collection(name='articles')

        # The client sends json data to the likes endpoint asynchronously using jquery, then
        # we receive the data and then reply the client with a json data
        # which is rendered in the template file using javascript
        slug_id = str(request.form.get('slug', type=str))
        likes = int(request.form.get('no_likes', 0, type=int))

        # Execute query to update data
        articles.find_one_and_update(
            {'slug': slug_id},
            {'$inc': {'likes': likes}}
        )
        query = articles.find_one({'slug': slug_id}, {"likes": 1})
        result = query['likes']
        return {'result': result}
