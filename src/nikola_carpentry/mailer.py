import smtplib
from nikola_carpentry import app, Contact
from email.mime.text import MIMEText

HOST = app.config["SMTP_HOST"]
PORT = app.config["SMTP_PORT"]
SERVICE_USER = app.config["SMTP_SERVICE_USER"]
SERVICE_PASSWORD = app.config["SMTP_SERVICE_PASSWORD"]
NOTIFICATION_RECIPIENTS = app.config["NOTIFICATION_RECIPIENTS"]


def send_contact_email(contact: Contact) -> None:
    msg = MIMEText(contact.content)
    msg["Subject"] = contact.subject
    msg["To"] = ", ".join(NOTIFICATION_RECIPIENTS)
    msg["From"] = SERVICE_USER

    with smtplib.SMTP(HOST, PORT) as server:
        server.login(SERVICE_USER, SERVICE_PASSWORD)
        server.sendmail(msg["From"], msg["To"], msg.as_string())

    print("Message sent!")
