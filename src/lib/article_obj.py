from .link_processor import LinkProcessor

class ArticleObj:
    def __init__(self, headline, link):
        self.headline = headline
        self.link = link

    @classmethod
    def create_article_objects(cls, link_elements):
        articles = []
        for link in link_elements:
            article_link = LinkProcessor.process(link.get('href'))
            articles.append(cls(link.text, article_link))

        return articles
