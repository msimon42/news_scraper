from application import mail
from flask import render_template
from flask_mail import Message

class ConfirmationMailer:
    @classmethod
    def send_message(cls, recipient_email, recipient_token):
        message = Message('News Scraper -- Confirm your Subscription',
                           recipients=[recipient_email],
                           sender='confirm@news-scraper.com')

        message.html = render_template('mail_templates/confirmation.html', uid=recipient_token)
        mail.send(message)

class ArticlesMailer:
    @classmethod
    def send_message(cls, recipient, articles):
        message = Message("News Scraper -- Today's articles",
                           recipients=[recipient.email],
                           sender='news@news-scraper.com')

        message.html = render_template('mail_templates/daily_articles.html', uid=recipient.token, articles=articles)
        mail.send(message)

class UpdateMailer:
    @classmethod
    def send_message(cls, recipient_email, recipient_token, **kwargs):
        message = Message(
                'Your Subscription Update',
                recipients=[recipient_email],
                sender='noreply@news-scraper.com'
        )

        message.html = render_template('mail_templates/update.html', uid=recipient_token,
                    link_actions=kwargs['link_actions'], email_actions=kwargs['email_actions'], filter_actions=kwargs['filter_actionss'])

        mail.send(message)
