# Local modules

# User-defined modules

# Third-party modules
from wtforms import StringField, validators, TextAreaField, PasswordField, SelectField
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField


# Form for Comments
class CommentForm(FlaskForm):
    comment_name = StringField('Name *', [
        validators.InputRequired(),
        validators.DataRequired(),
        validators.Length(min=5, max=30)
    ])
    comment_msg = TextAreaField('Message *', [
        validators.InputRequired(),
        validators.DataRequired(),
        validators.Length(min=1, max=255)
    ])


# Form for Blog Post
class ArticleForm(FlaskForm):
    title = StringField('Title', [
        validators.InputRequired(),
        validators.Length(max=225),
        validators.DataRequired()
    ])
    keywords = StringField('Keywords', [
        validators.InputRequired(),
        validators.Length(min=7, max=250),
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
    readTime = StringField('Read Time (in Min)', [
        validators.DataRequired(),
        validators.InputRequired(),
        validators.Length(max=2)
    ])
    status = SelectField('Status', [validators.DataRequired()], choices=[
        ('draft', 'Draft'),
        ('published', 'Published')
    ], default='draft')


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
        validators.Length(min=12)
    ])
    bio = TextAreaField('Biography *', [
        validators.InputRequired(),
        validators.DataRequired(),
        validators.Length(min=1, max=255)
    ])
