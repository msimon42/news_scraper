from flask import Flask, request, render_template, redirect, flash
from flask_mail import Mail, Message
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from src.lib.article_serializer import ArticleSerializer
from src.forms import *
from dotenv import load_dotenv
import os



def create_application(test_config=None):
    application = Flask(__name__, instance_relative_config = True)

    application.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL"),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        MAIL_SERVER = 'smtp.sendgrid.net',
        MAIL_PORT = 587,
        MAIL_USE_TLS = True,
        MAIL_USERNAME = 'apikey',
        MAIL_PASSWORD = os.getenv('SENDGRID_API_KEY'),
        MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    )


    try:
        os.makedirs(application.instance_path)
    except OSError:
        pass

    @application.route('/')
    def root():
        return render_template('landing.html')

    @application.route('/confirm', methods=['GET', 'POST'])
    def confirm():
        token = request.args.get('token')
        user = User.query.filter_by(token=token).scalar()
        user.confirmed = True
        db.session.commit()
        return render_template('confirmation_return.html')

    @application.route('/subscribe', methods=['GET', 'POST'])
    def subscribe():
        form = SubscriptionForm()
        if form.validate_on_submit():
            email_address = request.form['email']
            links = request.form['links'].split(',')

            new_user = User(email=email_address)
            db.session.add(new_user)
            db.session.commit()

            for link in links:
                link_ = Link.query.filter_by(url=link).scalar()
                if link_ is None:
                    try:
                        response = subscription_attempt(link, new_user)
                        flash(response)
                    except:
                        flash(f"Could not connect to {link}. All urls must be preceded by 'http://' or 'https://'.")

                    continue

                us = UserSubscription(link_id=link_.id, user_id=new_user.id)
                db.session.add(us)
                db.session.commit()

            flash('You are subscribed to news scraper!')
            send_confirmation_email.delay(new_user.email, new_user.token)
            return redirect('/')

        return render_template('subscribe.html', title='Subscribe', form=form)

    @application.route('/unsubscribe')
    def unsubscribe():


    @application.route('/api/request-articles', methods=['POST'])
    def request_articles():
        data = request.json
        articles = Scraper.get_articles(data['url'], data['css-tag'])
        return ArticleSerializer.render_json(articles)

    ## HELPER METHODS ##

    def subscription_attempt(link, user):
        status_code = Scraper.ping(link)
        if status_code == 200:
            new_link = Link(url=link)
            db.session.add(new_link)
            db.session.commit()
            us = UserSubscription(link_id=new_link.id, user_id=user.id)
            db.session.add(us)
            db.session.commit()
            return f'Subscribed to {link}'
        else:
            return f'Could not subscribe to {link}. It is possible that this site blocks web scraping.'


    return application

application = create_application()
db = SQLAlchemy(application)
mail = Mail(application)

from src.models import *
from src.mailers import *
from tasks import *
from src.lib.scraper import Scraper


if __name__ == '__main__':
    application.run(host='0.0.0.0')
