from flask_script import Command
from application import db
from src.models import *
from src.mailers import *
from src.lib.css_finder import CssFinder
import os

class GetArticles(Command):
    "Gets articles from all links in db"

    def run(self):
        links = Link.with_valid_css_tag()

        for link in links:
            try:
                user_agent = UserAgent.random_user_agent_header()
                articles = Scraper().get_articles(link.url, link.css_tag, user_agent)
                for article in articles:
                    exists = Article.query.filter_by(url=article.link).scalar()
                    if exists is None:
                        new_article = Article(link_id=self.id,
                                              url=article.link,
                                              headline=article.headline)

                        db.session.add(new_article)
                        db.session.commit()
                    else:
                        continue
                print(f'Articles collected for {link.url}')
            except:
                print(f'Failed to collect articles for {link.url}. Please contact your systems administrator.')

        print('done')

class FillCssTags(Command):
    "Finds all missing css tags for links in db"

    def run(self):
        links = Link.with_empty_css_tag()
        css_finder = CssFinder()
        for link in links:
            url = link.url
            try:
                tag = css_finder.find_tag(url)
                print(f'Collected tag for {url}')
            except:
                tag = 'no tag'
                print(f'Could not find tag for {url}')

            link.css_tag = tag
            db.session.commit()

        print('done')

class SendArticlesToUsers(Command):
    "Sends articles to users"

    def run(self):
        articles = Article.from_n_days_ago(2)
        users = User.confirmed_users()

        for user in users:
            user_articles = user.select_articles_for_today(articles)
            ArticlesMailer.send_message(user, user_articles)
            user.add_sent_articles(user_articles)
            print(f'Sent articles to {user.email}')

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
        try:
            email = os.getenv('ADMIN_EMAIL')
            token = os.getenv('ADMIN_TOKEN')
            ConfirmationMailer.send_message(email, token)
            print('Done')
        except:
            print('An exception occured.')
