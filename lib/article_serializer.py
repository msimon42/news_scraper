from flask import jsonify


class ArticleSerializer:
    @classmethod
    def render_json(cls, articles):
        modded_articles = map(cls.convert_article_to_dict(), articles)

    @classmethod
    def convert_article_to_dict(cls, article):
        return {'headline':article.headline, 'link':article.link}
