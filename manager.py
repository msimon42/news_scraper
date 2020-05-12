from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from src.models import *
from src.scripts import *

migrate = Migrate(app, db)
manager = Manager(app)

def make_shell_context():
    return dict(app=app,
                db=db,
                User=User,
                Link=Link,
                UserSubscription=UserSubscription,
                Article=Article,
                SentArticle=SentArticle)

manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('get todays articles', GetArticles())


if __name__ == '__main__':
    manager.run()
