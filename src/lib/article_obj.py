from .link_processor import LinkProcessor
from src.models import *
from datetime import datetime

class ArticleObj:
    def __init__(self, headline, url):
        self.headline = headline
        self.url = url
        self.created_at = datetime.now()

    def save_to_db(self, link_id):
        exists = Article.query.filter_by(url=self.url).scalar()
        if exists is None:
            a = Article(link_id=link_id, url=self.url, headline=self.headline)
            db.session.add(a)
            db.session.commit()

    @classmethod
    def create_article_objects(cls, link_elements):
        articles = []
        for link in link_elements:
            article_link = LinkProcessor.process(link.get('href'))
            articles.append(cls(link.text, article_link))

        return articles
