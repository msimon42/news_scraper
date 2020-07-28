from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_mail import Mail, Message
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from src.lib.article_serializer import ArticleSerializer
from src.lib.articles_request_validator import ArticlesRequestValidator
from src.lib.css_finder import CssFinder
from src.forms import *
from dotenv import load_dotenv
import os
import json
import numpy as np


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
            links = request.form['links']

            new_user = User(email=email_address)
            db.session.add(new_user)
            db.session.commit()

            actions = update_links(new_user, links)

            flash('You are subscribed to news scraper!')
            send_confirmation_email.delay(new_user.email, new_user.token)
            return redirect('/')

        return render_template('subscribe.html', title='Subscribe', form=form)

    @application.route('/unsubscribe')
    def unsubscribe():
        user = User.find_by_token(request.args.get('token'))
        user.confirmed = False
        db.session.commit()
        return render_template('unsubsrcibe_return.html')

    @application.route('/dashboard', methods=['GET', 'POST'])
    def dashboard():
        user = User.find_by_token(request.args.get('token'))
        form = DashboardForm()
        form.email.data = user.email
        form.links.data = ','.join(user.link_urls())
        form.filters.data = ','.join(user.filters())

        if form.validate_on_submit():
            form_data = {
                'email': request.form['email'],
                'links': request.form['links'],
                'filters': request.form['filters']
            }

            update_user(user, form_data)

        return render_template('dashboard.html', form=form)


    @application.route('/api/v1/scrape-articles', methods=['POST'])
    def scrape_articles():
        data = request.get_json(force=True)

        if Scraper.ping(data['url']) == 200:
            tag = CssFinder().find_tag(data['url'])
            link = Link(url=data['url'], css_tag=tag)
            db.session.add(link)
            db.session.commit()

            articles = Scraper().get_articles(data['url'], tag, save=True, link_id=link.id, user_agent=None)
            return ArticleSerializer.render_json(articles)

        return jsonify('Invalid URL'), 400


    @application.route('/api/v1/articles', methods=['POST'])
    def request_articles():
        data = request.get_json(force=True)
        validated_request = ArticlesRequestValidator.validate(data)

        if validated_request is not None:
            articles = Article.api_query(validated_request)
            return ArticleSerializer.render_json(articles)

        return jsonify('Invalid request. Please read the docs and try again.'), 400




    ## HELPER METHODS ##

    def subscription_attempt(link, user_token):
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


    def update_user(user, form_data):
        update_links(user, form_data['links'])
        update_email(user, form_data['email'])[user.email == form_data['email']]
        update_filters(user, form_data['filters'])

    def update_email(user, new_email):
        return {
            False: user.update_email(new_email),
            True: do_nothing()
        }

    def update_filters(user, filters):
        filters = filters.split(',')
        current_filters = user.filters()

        new_filters = np.setdiff1d(filters,current_filters)
        removed_filters = np.setdiff1d(current_filters,filters)

        for filter in new_filters:
            filter_ = Filter.find_by_word(filter)
            if filter_ is None:
                new_filter = Filter(word=filter)
                db.session.add(new_filter)
                db.session.commit()
                new_user_filter = UserFilter(user_id=user.id, filter_id=new_filter.id)
                db.session.add(new_user_filter)
                db.session.commit()
            else:
                new_user_filter = UserFilter(user_id=user.id, filter_id=filter_.id)
                db.session.add(new_user_filter)
                db.session.commit()

        for filter in removed_filters:
            filter_ = filter.find_by_word(filter)
            user_filter = UserFilter.query.filter_by(user_id=user.id, filter_id=filter_.id).scalar()
            db.session.delete(user_filter)
            db.session.commit()

    def update_links(user, links):
        links_list = links.split(',')
        user_links = user.link_urls()
        actions = []

        new_links = np.setdiff1d(links_list,user_links)
        unsubed_links = np.setdiff1d(user_links,links_list)

        for link in new_links:
            link_ = Link.find_by_url(link)
            if link_ is None:
                try:
                    response = subscription_attempt(link, user)
                    actions.append(response)
                except:
                    actions.append(f"Could not connect to {link}. All urls must be preceded by 'http://' or 'https://'.")

                continue

            us = UserSubscription(link_id=link_.id, user_id=user.id)
            db.session.add(us)
            db.session.commit()

        for link in unsubed_links:
            link_ = Link.find_by_url(link)
            us = UserSubscription.query.filter_by(link_id=link_.id, user_id=user.id).scalar()
            db.session.delete(us)
            db.session.commit()
            actions.append(f'Unsubscribed from {link}')

        return actions

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
