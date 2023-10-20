from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed  # TODO: Not working as intended
from wtforms import (
    StringField,
    SubmitField,
    PasswordField,
    SelectField,
    BooleanField,
    MultipleFileField,
    SelectMultipleField,
)
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, InputRequired
from nikola_carpentry.app import app
from nikola_carpentry.models import Tag


class UserForm(FlaskForm):
    username = StringField("User Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    email = StringField("Email Address", validators=[DataRequired()])
    submit = SubmitField("Create User")


class TagForm(FlaskForm):
    tag_name = StringField("Tag Name", validators=[DataRequired()])
    submit = SubmitField("Create Tag")


class LoginForm(FlaskForm):
    username = StringField("User Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Submit!")


class ContactForm(FlaskForm):
    subject = StringField("Subject")
    contact_name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email Address")
    phone = StringField("Phone Number")
    content = CKEditorField("Write a message", validators=[DataRequired()])
    submit = SubmitField("Send contact request!")


class ProjectForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = CKEditorField("Content", validators=[DataRequired()])
    files = MultipleFileField()
    with app.app_context():
        tag_list: list[Tag] = Tag.query.all()
        tags = [(tag.tag_name, tag.tag_name) for tag in tag_list]

    tags = SelectMultipleField(
        "Tags",
        choices=tags,
        validators=[InputRequired()],
    )
    submit = SubmitField("Submit!")


class ReviewForm(FlaskForm):
    author = StringField("Name")
    title = StringField("Title", validators=[DataRequired()])
    rating = SelectField(
        "Rating",
        choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")],
        validators=[InputRequired()],
    )
    content = CKEditorField("Content", validators=[DataRequired()])
    submit = SubmitField("Submit!")
