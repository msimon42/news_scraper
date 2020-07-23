from .link_processor import LinkProcessor
from src.models import *

class ArticleObj:
    def __init__(self, headline, url):
        self.headline = headline
        self.url = url

    def save_to_db(self, link_id):
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
