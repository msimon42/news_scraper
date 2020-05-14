from celery import Celery
from application import celery, application
from src.mailers import *

@celery.task(name='tasks.send_confirmation_email')
def send_confirmation_email(recip_email, recip_id):
    ConfirmationMailer.send_message(recip_email, recip_id)
