from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed  #TODO: Not working as intended
from wtforms import (
    StringField,
    SubmitField,
    PasswordField,
    BooleanField,
    MultipleFileField,
)
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("User Name: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Submit!")


class ContactForm(FlaskForm):
    contact_name = StringField("Name: ", validators=[DataRequired()])
    submit = SubmitField("Submit!")


class ProjectForm(FlaskForm):
    title = StringField("Title: ", validators=[DataRequired()])
    content = CKEditorField("Content: ", validators=[DataRequired()])
    files = MultipleFileField(FileAllowed(["jpg, png"], "Images only!"))
    submit = SubmitField("Submit!")


class ReviewForm(FlaskForm):
    author = StringField("Name: ")
    title = StringField("Review title: ", validators=[DataRequired()])
    content = CKEditorField("Content: ", validators=[DataRequired()])
    submit = SubmitField("Submit!")
