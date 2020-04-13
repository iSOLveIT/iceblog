from wtforms import Form, StringField, validators
from flask_ckeditor import CKEditorField
from wtforms.fields.html5 import EmailField


# Form for Blog Form
class ArticleForm(Form):
    title = StringField('Title', [
        validators.Length(max=225),
        validators.DataRequired()
    ])
    body = CKEditorField('Body', [
        validators.DataRequired(),
        validators.Length(min=30)
    ])
    link = StringField('Link to Cover Image', [
        validators.DataRequired(),
        validators.InputRequired(message="Please provide link to the image"),
    ])

