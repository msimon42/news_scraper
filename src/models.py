from ..app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)

    subscribed_links = db.relationship('Link', backref='user')

    def __repr__():
        'User %r' % self.email


class Link(db.Model):
    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    css_tag = db.Column(db.String)

    def __repr__():
        'Link %r' % self.url   
