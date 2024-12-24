# HomeMate/server/app/tasks/template.py

from flask import current_app
from flask_mail import Message

def send_email(to_email, subject, body, is_html=False):
    from .. import mail
    sender = (current_app.config['MAIL_NAME'], current_app.config['MAIL_USERNAME'])
    msg = Message(subject, sender=sender, recipients=[to_email])
    if is_html:
        msg.html = body 
    else:
        msg.body = body
    mail.send(msg)

def send_email_with_doc(to_email, subject, body, pdf_attachment):
    from .. import mail
    sender = (current_app.config['MAIL_NAME'], current_app.config['MAIL_USERNAME'])
    msg = Message(subject, sender=sender, recipients=[to_email])
    msg.html = body
    msg.attach("monthly_report.pdf", "application/pdf", pdf_attachment)
    mail.send(msg)

def send_email_with_csv(to_email, subject, body, csv_attachment):
    from .. import mail
    sender = (current_app.config['MAIL_NAME'], current_app.config['MAIL_USERNAME'])
    msg = Message(subject, sender=sender, recipients=[to_email])
    msg.html = body
    msg.attach("completed_service_request.csv", "text/csv", csv_attachment)
    mail.send(msg)