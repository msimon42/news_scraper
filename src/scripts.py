from flask_script import Command
from application import db
from src.models import *
from src.mailers import *
from src.lib.css_finder import CssFinder
from src.lib.scraper import Scraper
from src.lib.nl_processor import NLProcessor
from src.lib.timer import Timer
import os

class GetArticles(Command):
    "Gets articles from all links in db"

    def run(self):
        links = Link.with_valid_css_tag()
        scraper = Scraper()
        t = Timer()
        for link in links:
            try:
                user_agent = UserAgent.random_user_agent_header()
                articles = scraper.get_articles(link.url, link.css_tag, user_agent=user_agent, save=True, link_id=link.id)

                et = t.stop()
                print(f"{len(articles)} articles collected for {link.url} in {et:0.4f} seconds")
                t.reset()
            except:
                print(f'Failed to collect articles for {link.url}. Please contact your systems administrator.')
                t.reset()

        print('done')

class FillCssTags(Command):
    "Finds all missing css tags for links in db"

    def run(self):
        links = Link.with_empty_css_tag()
        css_finder = CssFinder()
        t = Timer()
        for link in links:
            headers = UserAgent.random_user_agent_header()
            url = link.url

            try:
                tag = css_finder.find_tag(url, headers)
                et = t.stop()
                print(f'Collected tag for {url} in {et:0.4f} seconds')
                t.reset()
            except:
                tag = 'no tag'
                print(f'Could not find tag for {url}')
                t.reset()

            link.css_tag = tag
            db.session.commit()

        print('done')

class SendArticlesToUsers(Command):
    "Sends articles to users"

    def run(self):
        articles = Article.from_n_days_ago(2)
        users = User.confirmed_users()
        t = Timer()

        for user in users:
            user_articles = user.select_articles_for_today(articles)
            ArticlesMailer.send_message(user, user_articles)
            user.add_sent_articles(user_articles)
            et = t.stop()
            print(f'Sent articles to {user.email} in {et:0.4f} seconds')
            t.reset()

        print('Done.')

class TestNewsletter(Command):
    "Sends a test newsletter"

    def run(self):
        articles = Article.from_n_days_ago(2)
        user = User.query.get(18)
        user_articles = user.select_articles_for_today(articles)
        ArticlesMailer.send_message(user, user_articles)

        print('Done')

class TestConfirmationEmail(Command):
    "Sends a test confirmation email"

    def run(self):
        email = os.getenv('ADMIN_EMAIL')
        token = os.getenv('ADMIN_TOKEN')
        ConfirmationMailer.send_message(email, token)

        print('Done')


class CleanArticleHeadlines(Command):
    "Removes unnessesary spaces, tabs, and line breaks from article headlines"

    def run(self):
        nlp = NLProcessor()
        articles = Article.query.all()

        for article in articles:
            article.headline = nlp.preprocess_phrase(article.headline)

        print('Done')
