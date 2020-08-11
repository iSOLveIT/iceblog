from wtforms import StringField, validators, TextAreaField, PasswordField
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField


# Form for Comments
class CommentForm(FlaskForm):
    name = StringField('Name *', [
        validators.InputRequired(),
        validators.DataRequired(),
        validators.Length(min=5, max=30)
    ])
    msg = TextAreaField('Message *', [
        validators.InputRequired(),
        validators.DataRequired(),
        validators.Length(min=1, max=255)
    ])


# Form for Blog Post
class ArticleForm(FlaskForm):
    title = StringField('Title', [
        validators.Length(max=225),
        validators.DataRequired()
    ])
    body = CKEditorField('Body', [
        validators.DataRequired(),
        validators.InputRequired(),
        validators.Length(min=30)
    ])
    category = StringField('Category', [
        validators.DataRequired(),
        validators.InputRequired(message="Please provide category for article"),
        validators.Length(max=15)
    ])
    readTime = StringField('Minutes spent reading', [
        validators.DataRequired(),
        validators.InputRequired(),
        validators.Length(max=2)
    ])


# Form for Login
class SignupForm(FlaskForm):
    first_name = StringField('First Name *', [
        validators.InputRequired(),
        validators.DataRequired(),
        validators.Length(min=5, max=30)
    ])

    last_name = StringField('Last Name *', [
        validators.InputRequired(),
        validators.DataRequired(),
        validators.Length(min=5, max=30)
    ])

    email = EmailField('Email Address', [
        validators.InputRequired(),
        validators.DataRequired(),
        validators.Length(min=20, max=100)
    ])

    username = StringField('Username *', [
        validators.InputRequired(),
        validators.DataRequired(),
        validators.Length(min=5, max=30)
    ])

    password = PasswordField('Password *', [
        validators.InputRequired(),
        validators.DataRequired(),
        validators.Length(min=8, max=30)
    ])
    bio = TextAreaField('Biography *', [
        validators.InputRequired(),
        validators.DataRequired(),
        validators.Length(min=1, max=255)
    ])
