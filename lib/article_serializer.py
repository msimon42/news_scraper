from flask import jsonify


class ArticleSerializer:
    @classmethod
    def render_json(cls, articles):
        pass

    @classmethod
    def convert_article_to_dict(cls, article):
        return {'headline':article.headline, 'link':article.link}
