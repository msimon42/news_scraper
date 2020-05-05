from flask import Flask, request, render_template
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from src.lib.scraper import Scraper
from src.lib.article_serializer import ArticleSerializer
from src.forms import *
from dotenv import load_dotenv
import os


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config = True)

    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL"),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def root():
        return render_template('landing.html')

    @app.route('/subscribe', methods=['GET', 'POST'])
    def subscribe():
        form = SubscriptionForm()
        return render_template('subscribe.html', title='Subscribe', form=form)

    @app.route('/api/request-articles', methods=['POST'])
    def request_articles():
        data = request.json
        articles = Scraper.get_articles(data['url'], data['css-tag'])
        return ArticleSerializer.render_json(articles)

    return app

app = create_app()
db = SQLAlchemy(app)
from src.models import *


if __name__ == '__main__':
    app.run(host='0.0.0.0')
