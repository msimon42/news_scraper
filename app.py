from flask import Flask
from news_scraper.lib.scraper import Scraper
from news_scraper.lib.article_serializer import ArticleSerializer
from dotenv import load_dotenv
import os




def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config = True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL"),
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def root():
        return "You're connected to news_scraper!"

    @app.route('/request-articles')
    def request_articles():
        articles = Scraper.get_slashdot_articles()
        return ArticleSerializer.render_json(articles)

    return app

app = create_app()
