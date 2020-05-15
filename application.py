from flask import Flask, request, render_template, redirect, flash
from flask_mail import Mail, Message
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from src.lib.scraper import Scraper
from src.lib.article_serializer import ArticleSerializer
from src.lib.css_finder import CssFinder
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
        id = request.args.get('id')
        user = User.query.get(id)
        user.confirmed = True
        db.session.commit()
        return 'Your subscription has been confirmed!'

    @application.route('/subscribe', methods=['GET', 'POST'])
    def subscribe():
        form = SubscriptionForm()
        if form.validate_on_submit():
            email_address = request.form['email']
            links = request.form['links'].split(',')

            new_user = User(email=email_address)
            db.session.add(new_user)
            db.session.commit()

            send_confirmation_email.delay(new_user.email, new_user.id)

            for link in links:
                link_ = Link.query.filter_by(url=link).first()
                if link_ is None:
                    try:
                        css_tag = CssFinder.find_tag(link)
                        new_link = Link(url=link, css_tag=css_tag)
                        db.session.add(new_link)
                        db.session.commit()
                        us = UserSubscription(link_id=new_link.id, user_id=new_user.id)
                        db.session.add(us)
                        db.session.commit()
                    except:
                        flash(f"Could not subscribe to {link}. It's possible that this site blocks web scraping.")

                    continue

                us = UserSubscription(link_id=link_.id, user_id=new_user.id)
                db.session.add(us)
                db.session.commit()

            flash('You are subscribed to news scraper!')
            return redirect('/')

        return render_template('subscribe.html', title='Subscribe', form=form)

    @application.route('/api/request-articles', methods=['POST'])
    def request_articles():
        data = request.json
        articles = Scraper.get_articles(data['url'], data['css-tag'])
        return ArticleSerializer.render_json(articles)

    return application

application = create_application()
db = SQLAlchemy(application)
mail = Mail(application)

with application.app_context():
    celery = Celery(__name__, broker=f"sqs://{os.environ['AWS_ACCESS_KEY_ID']}:{os.environ['AWS_ACCESS_KEY']}@")
    celery.conf.update(application.config)

from src.models import *
from src.mailers import *
from tasks import *

if __name__ == '__main__':
    application.run(host='0.0.0.0')