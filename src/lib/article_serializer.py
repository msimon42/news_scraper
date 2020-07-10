from flask import jsonify

class ArticleSerializer:
    @classmethod
    def render_json(cls, articles):
        modded_articles = list(map(cls.convert_article_to_dict, articles))
        return jsonify({'Data': modded_articles})

    @classmethod
    def convert_article_to_dict(cls, article):
        return {
                'headline': article.headline,
                'url': article.url,
                'date': article.created_at
               }
