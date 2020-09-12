from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from application import application, db
from src.models import *
from src.scripts import *

migrate = Migrate(application, db)
manager = Manager(application)

def make_shell_context():
    return dict(application=application,
                db=db,
                User=User,
                Link=Link,
                UserSubscription=UserSubscription,
                Article=Article,
                SentArticle=SentArticle,
                UserAgent=UserAgent,
                Filter=Filter,
                UserFilter=UserFilter)

manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('get-todays-articles', GetArticles())
manager.add_command('fill-tags', FillCssTags())
manager.add_command('send-articles', SendArticlesToUsers())
manager.add_command('test-newsletter', TestNewsletter())
manager.add_command('test-confirmation', TestConfirmationEmail())
manager.add_command('clean-headlines', CleanArticleHeadlines())


if __name__ == '__main__':
    manager.run()
