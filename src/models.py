from app import db
from datetime import datetime
from lib.scraper import Scraper
from lib.nl_processor import NLProcessor

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    subscribed_links = db.relationship('UserSubscription', backref='user')
    recieved_articles = db.relationship('SentArticle', backref='user')

    def __repr__(self):
        'User %r' % self.email


class Link(db.Model):
    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    css_tag = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    subscribed_users = db.relationship('UserSubscription', backref='link')
    articles = db.relationship('Article', backref='link')

    def get_todays_articles(self):
        articles = Scraper.get_articles(self.url, self.css_tag)

        for article in articles:
            if NLProcessor.is_sentence(article.headline):
                new_article = Article(link_id=self.id,
                                      url=article.link,
                                      headline=article.headline)
                db.session.add(new_article)
                db.session.commit()


    def __repr__(self):
        'Link %r' % self.url


class UserSubscription(db.Model):
    __tablename__ = 'user_subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    link_id = db.Column(db.Integer, db.ForeignKey('links.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        'UserSubscription %r' % self.id


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    link_id = db.Column(db.Integer, db.ForeignKey('links.id'))
    url = db.Column(db.String)
    headline = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    recipients = db.relationship('SentArticle', backref='article')

    def __repr__(self):
        'Article %r' % self.headline


class SentArticle(db.Model):
    __tablename__ = 'sent_articles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        'SentArticle, %r' % self.id
