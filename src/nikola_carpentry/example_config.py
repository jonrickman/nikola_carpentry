from pathlib import Path


config = {
    # database stuff
    "SQLALCHEMY_DATABASE_URI": "sqlite:///app.db",
    "SECRET_KEY": "password",
    # file stuff
    "ROOT": Path(__file__).parent,
    "UPLOAD_FOLDER": "static",
    "MAX_CONTENT_LENGTH": 25 * 1000 * 1000,
    # Email settup
    "SMTP_HOST": "",
    "SMTP_PORT": "",
    "SMTP_SERVICE_USER": "",
    "SMTP_SERVICE_PASSWORD": "",
    "NOTIFICATION_RECIPIENTS": [],
}
