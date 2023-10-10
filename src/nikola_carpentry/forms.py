from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
from nikola_carpentry import app


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
    files = FileField()
    # FileAllowed(['jpg, png'], 'Images only!')])
    submit = SubmitField("Submit!")

    def save_files(self) -> str:
        """
        Save the files from project form
        """
        file_to_upload = self.files.data
        basename = secure_filename(file_to_upload.filename)
        file_root = app.config["ROOT"]
        upload_folder = app.config["UPLOAD_FOLDER"]
        filepath = file_root / upload_folder / basename
        file_to_upload.save(filepath)
        return basename


class ReviewForm(FlaskForm):
    author = StringField("Name: ")
    title = StringField("Review title: ", validators=[DataRequired()])
    content = CKEditorField("Content: ", validators=[DataRequired()])
    submit = SubmitField("Submit!")
