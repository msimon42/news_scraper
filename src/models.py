from src.lib.helper_methods import *
from application import db
from datetime import datetime, timedelta
from src.lib.nl_processor import NLProcessor
from sqlalchemy.sql import func
import random
import secrets

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    confirmed = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, default=secrets.token_urlsafe())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    subscribed_links = db.relationship('UserSubscription', backref='user')
    recieved_articles = db.relationship('SentArticle', backref='user')

    @classmethod
    def confirmed_users(cls):
        return cls.query.filter_by(confirmed=True)

    @classmethod
    def find_by_token(cls, token):
        return cls.query.filter_by(token=token).scalar()

    def sent_article_ids(self, days_ago):
        result = db.engine.execute('SELECT articles.id FROM articles ' +
                                   'INNER JOIN sent_articles ON sent_articles.article_id = articles.id ' +
                                   'INNER JOIN users ON sent_articles.user_id = users.id ' +
                                   f'WHERE users.id = {self.id} ' +
                                   f"AND articles.created_at > '{n_days_ago(days_ago)}'")

        return [ article.id for article in result ]

    def link_ids(self):
        result = db.engine.execute('SELECT links.id FROM links ' +
                                   'INNER JOIN user_subscriptions ON links.id = user_subscriptions.link_id ' +
                                   'INNER JOIN users ON users.id = user_subscriptions.user_id ' +
                                   f'WHERE users.id = {self.id}')

        ids = [ link.id for link in result ]
        return ids

    def select_articles_for_today(self, articles):
        article_ids = self.sent_article_ids(2)
        links = self.link_ids()

        eligible_articles = [ article for article in articles if article.link_id in links and article.id not in article_ids]
        try:
            return random.sample(eligible_articles, 10)
        except:
            return eligible_articles

    def not_yet_sent(self, article_id):
        sent_ids = self.sent_article_ids(2)
        return article_id not in sent_ids

    def add_sent_articles(self, articles):
        for article in articles:
            sent_article = SentArticle(user_id=self.id, article_id=article.id)
            db.session.add(sent_article)
            db.session.commit()

    def __repr__(self):
        return 'User %r' % self.id


class Link(db.Model):
    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    css_tag = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    subscribed_users = db.relationship('UserSubscription', backref='link')
    articles = db.relationship('Article', backref='link')


    def articles_from_n_days(self, n):
        n_days_ago = n_days_ago(n)
        return Article.query.filter(Article.link_id==self.id, Article.created_at>=n_days_ago)

    @classmethod
    def with_empty_css_tag(cls):
        return cls.query.filter_by(css_tag=None)

    @classmethod
    def with_valid_css_tag(cls):
        return cls.query.filter(cls.css_tag!='no tag', cls.css_tag!=None)

    @classmethod
    def find_by_url(cls, url):
        cls.query.filter_by(url=url).scalar()


    def __repr__(self):
        return 'Link %r' % self.url


class UserSubscription(db.Model):
    __tablename__ = 'user_subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    link_id = db.Column(db.Integer, db.ForeignKey('links.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return 'UserSubscription %r' % self.id


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    link_id = db.Column(db.Integer, db.ForeignKey('links.id'))
    url = db.Column(db.String, unique=True)
    headline = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    recipients = db.relationship('SentArticle', backref='article')

    @classmethod
    def from_n_days_ago(cls, days):
        cutoff = n_days_ago(days)
        return cls.query.filter(cls.created_at>=cutoff)

    def __repr__(self):
        return 'Article %r' % self.headline


class SentArticle(db.Model):
    __tablename__ = 'sent_articles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return 'SentArticle, %r' % self.id

class UserAgent(db.Model):
    __tablename__ = 'user_agents'

    id = db.Column(db.Integer, primary_key=True)
    agent_string = db.Column(db.String)

    @classmethod
    def random_user_agent_header(cls):
        random_agent = cls.query.order_by(func.random()).first()
        return {'User-Agent':random_agent.agent_string}

    def __repr__(self):
        return 'User Agent %r' % self.agent_string


class Filter(db.Model):
    __tablename__ = 'filters'

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String)

    def __repr__(self):
        return 'Filter %r' % self.word
