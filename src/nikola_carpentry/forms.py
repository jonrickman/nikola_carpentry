from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
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


class ReviewForm(FlaskForm):
    author = StringField("Name: ")
    title = StringField("Review title: ", validators=[DataRequired()])
    content = CKEditorField("Review text: ", validators=[DataRequired()])
    submit = SubmitField("Submit!")
    approved = BooleanField("Approve")
