from flask_script import Command
from application import db
from src.models import *
from src.lib.css_finder import CssFinder

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

class FillCssTags(Command):
    "Finds all missing css tags for links in db"

    def run(self):
        links = Link.with_empty_css_tag()

        for link in links:
            url = link.url
            try:
                tag = CssFinder.find_tag(url)
                print(f'Collected tag for {url}')
            except:
                tag = 'no tag'
                print(f'Could not find tag for {url}')

            link.css_tag = tag
            db.session.commit()

        print('done')
