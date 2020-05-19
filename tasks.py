from celery import Celery
from application import application
from src.mailers import *
import os

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=os.getenv['REDIS_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(application)

@celery.task(name='tasks.send_confirmation_email')
def send_confirmation_email(recip_email, recip_id):
    ConfirmationMailer.send_message(recip_email, recip_id)
