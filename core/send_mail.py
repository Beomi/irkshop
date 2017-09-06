from irkshop.celery import app
from django.conf import settings
from django.template.loader import render_to_string

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import smtplib


@app.task
def send_mail(user, pwd, recipient, subject, body):
    import smtplib
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body
    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(FROM, TO, message)
    server.close()
    return True


def send_gmail(send_to: str, subject: str, order):
    # First, you MUST activate SMTP for your Gmail Account
    if order.is_paid:
        rendered = str(render_to_string(
            template_name='mail_payment_confirm_template.html',
            context={
                'order': order,
            }
        ))
    else:
        rendered = str(render_to_string(
            template_name='mail_template.html',
            context={
                'order': order,
            }
        ))
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = settings.GMAIL_ID
    msg['To'] = send_to
    gmail_user = settings.GMAIL_ID
    gmail_pwd = settings.GMAIL_PW
    msg.attach(MIMEText(rendered, 'html'))
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(msg['From'], send_to, msg.as_string())
    server.close()
