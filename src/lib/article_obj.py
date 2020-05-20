class ArticleObj:
    def __init__(self, headline, link):
        self.headline = headline
        self.link = link

    @classmethod
    def create_article_objects(cls, link_elements):
        articles = []
        for link in link_elements:
            articles.append(cls(link.text, link.get('href')))

        return articles     
