from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from src.models import *

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
def make_shell_context():
    return dict(app=app,
                db=db,
                User=User,
                Link=Link,
                UserSubscription=UserSubscription,
                Article=Article,
                SentArticle=SentArticle)
