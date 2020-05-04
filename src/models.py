from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)

    subscribed_links = db.relationship('UserSubscription', backref='user')
    recieved_articles = db.relationship('SentArticle', backref='user')

    def __repr__():
        'User %r' % self.email


class Link(db.Model):
    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    css_tag = db.Column(db.String)

    subscribed_users = db.relationship('UserSubscription', backref='link')
    articles = db.relationship('Article', backref='link')

    def __repr__():
        'Link %r' % self.url


class UserSubscription(db.Model):
    __tablename__ = 'user_subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    link_id = db.Column(db.Integer, db.ForeignKey('links.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__():
        'UserSubscription %r' % self.id


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    link_id = db.Column(db.Integer, db.ForeignKey('links.id'))
    url = db.Column(db.String)
    headline = db.Column(db.String)

    recipients = db.relationship('SentArticle', backref='article')

    def __repr__():
        'Article %r' % self.headline


class SentArticle(db.Model):
    __tablename__ = 'sent_articles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))

    def __repr__():
        'SentArticle, %r' % self.id
