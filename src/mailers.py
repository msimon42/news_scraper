from application import mail
from flask import render_template
from flask_mail import Message

class ConfirmationMailer:
    @classmethod
    def send_message(cls, recipient):
        message = Message('News Scraper -- Confirm you email address',
                           recipients=[recipient.email])

        message.html = render_template('mail_templates/confirmation.html', uid=recipient.id)
        mail.send(message)
