from app import mail
from flask_mail import Message

class ConfirmationMailer:
    @classmethod
    def send(cls, recipient):
        message = Message('News Scraper -- Confirm you email address',
                           recipients=[recipient])

        message.html = render_template('mail_templates/confirmation.html', uid = recipient.id)
        mail.send(message)
