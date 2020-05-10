from wtforms import StringField, validators, TextAreaField, PasswordField
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
# from wtforms.fields.html5 import EmailField


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
    link = StringField('Cover Image Link', [
        validators.DataRequired(),
        validators.InputRequired(message="Please provide link to the image")
    ])
    category = StringField('Category', [
        validators.DataRequired(),
        validators.InputRequired(message="Please provide category for article")
    ])
    readTime = StringField('Minutes spent reading', [
        validators.DataRequired(),
        validators.InputRequired()
    ])


# Form for Comments
class CommentForm(FlaskForm):
    name = StringField('Name *', [
        validators.InputRequired(),
        validators.Length(min=5, max=30)
    ])
    msg = TextAreaField('Message *', [
        validators.InputRequired(),
        validators.Length(min=1, max=255)
    ])


# Form for Login
class LoginForm(FlaskForm):
    username = StringField('Username', [
        validators.InputRequired(),
        validators.Length(min=5, max=30)
    ])
    password = PasswordField('Password', [
        validators.InputRequired(),
        validators.Length(min=8, max=30)
    ])
