import json
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from flask_ckeditor import CKEditor


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
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SECRET_KEY"] = "password"
app.config["ROOT"] = Path(__file__).parent
app.config["UPLOAD_FOLDER"] = "static"
app.config["MAX_CONTENT-PATH"] = 25 * 1000 * 1000

db: SQLAlchemy = SQLAlchemy(model_class=Base, app=app)

# Configure Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

ckeditor = CKEditor(app)


if __name__ == "__main__":
    from nikola_carpentry.routes import *

    app.run(debug=True, host="0.0.0.0")
