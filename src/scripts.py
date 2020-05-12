from flask_script import Command
from src.models import *

class GetArticles(Command):
    "Gets articles from all links in db"

    def run(self):
        links = Link.query.all()

        for link in links:
            try:
                link.get_todays_articles()
                print(f'Articles collected for {link.url}')
            except:
                print(f'Failed to collect articles for {link.url}. Please contact your systems administrator.')    

        print('done')
