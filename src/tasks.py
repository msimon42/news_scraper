from celery import Celery
from app import app, celery
from mailers import *

@celery.task(name='tasks.send_confirmation email')
def send_confirmation_email(recip):
    ConfirmationMailer.send_message(recip)
