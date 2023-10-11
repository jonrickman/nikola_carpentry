from smtplib import SMTP
from nikola_carpentry import app, Contact

HOST = app.config["SMTP_HOST"]
PORT = app.config["SMTP_PORT"]
SERVICE_USER = app.config["SMTP_SERVICE_USER"]
SERVICE_PASSWORD = app.config["SMTP_SERVICE_PASSWORD"]
OUTGOING_EMAIL_ADDRESS = app.config["OUTGOING_EMAIL_ADDRESS"]


def send_contact_email(contact: Contact) -> None:
    with SMTP(HOST) as smtp:
        smtp.noop()
