import json

from flask import Flask
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from nikola_carpentry.config import config


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


app = Flask(__name__, template_folder="templates")

# Configure Database
app.config["SQLALCHEMY_DATABASE_URI"] = config["SQLALCHEMY_DATABASE_URI"]
app.config["SECRET_KEY"] = config["SECRET_KEY"]

# Configure file specifics
app.config["ROOT"] = config["ROOT"]
app.config["UPLOAD_FOLDER"] = config["UPLOAD_FOLDER"]
app.config["MAX_CONTENT_LENGTH"] = config["MAX_CONTENT_LENGTH"]

# Configure email settings
app.config["SMTP_HOST"] = config["SMTP_HOST"]
app.config["SMTP_PORT"] = config["SMTP_PORT"]
app.config["SMTP_SERVICE_USER"] = config["SMTP_SERVICE_USER"]
app.config["SMTP_SERVICE_PASSWORD"] = config["SMTP_SERVICE_PASSWORD"]
app.config["NOTIFICATION_RECIPIENTS"] = config["NOTIFICATION_RECIPIENTS"]

db: SQLAlchemy = SQLAlchemy(model_class=Base, app=app)

# Configure Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

ckeditor = CKEditor(app)


if __name__ == "__main__":
    from nikola_carpentry.routes import *

    app.run(debug=True, port=5001, host="0.0.0.0")
