from flask.views import MethodView
from flask import render_template


# View for index
class IndexEndpoint(MethodView):
    @staticmethod
    def get():
        return render_template('index.html'), 200


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
    def get():
        return render_template('category.html'), 200


# View for single blog
class SingleEndpoint(MethodView):
    @staticmethod
    def get():
        return render_template('single.html'), 200
