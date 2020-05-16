from application import db
from datetime import datetime, timedelta
from src.lib.scraper import Scraper
from src.lib.nl_processor import NLProcessor

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    confirmed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    subscribed_links = db.relationship('UserSubscription', backref='user')
    recieved_articles = db.relationship('SentArticle', backref='user')

    def sent_article_ids(self, days_ago):
        result = db.engine.execute('SELECT articles.id FROM articles ' +
                                   'INNER JOIN sent_articles ON sent_articles.article_id = articles.id ' +
                                   'INNER JOIN users ON sent_articles.user_id = users.id ' +
                                   f'WHERE users.id = {self.id} ' +
                                   f'AND articles.created_at > {datetime.now() - datetime.timedelta(days=days_ago)}')

        return [ article for article.id in result ]

    def links(self):
        result = db.engine.execute('SELECT links.id FROM links ' +
                                   'INNER JOIN user_subscriptions ON links.id = user_subscriptions.link_id ' +
                                   'INNER JOIN users ON users.id = user_subscriptions.user_id ' +
                                   f'WHERE users.id = {self.id}')

        ids = [ link.id for link in result ]
        return Link.query.filter(Link.id.in_(ids))

    def select_articles_for_today(self):
        article_ids = self.articles()
        links = self.links()





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

    def get_todays_articles(self):
        articles = Scraper().get_articles(self.url, self.css_tag)
        for article in articles:
            new_article = Article(link_id=self.id,
                                  url=article.link,
                                  headline=article.headline)
            db.session.add(new_article)
            db.session.commit()

    def articles_from_n_days(self, n):
        n_days_ago = (datetime.now() - timedelta(days=n)).strftime('%m-%d-%y')
        return Article.query.filter(Article.link_id==self.id, Article.created_at>=n_days_ago)

    @classmethod
    def with_empty_css_tag(cls):
        return cls.query.filter_by(css_tag=None)


    def __repr__(self):
        return 'Link %r' % self.id


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
    url = db.Column(db.String)
    headline = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    recipients = db.relationship('SentArticle', backref='article')

    def __repr__(self):
        return 'Article %r' % self.id


class SentArticle(db.Model):
    __tablename__ = 'sent_articles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return 'SentArticle, %r' % self.id
