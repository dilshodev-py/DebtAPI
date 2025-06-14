import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from root.celery import app
from root.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT, EMAIL_HOST

@app.task(bind=True)
def send_email(self,receiver_email , message_text):
    # sender_email = EMAIL_HOST_USER
    sender_email = 'absaitovdev@gmail.com'
    password = 'jyugxbqoubeoiohs'
    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email
    text = "salom"

    part1 = MIMEText(text, "plain")
    message.attach(part1)
    with smtplib.SMTP_SSL(sender_email, EMAIL_PORT) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )