from celery import Celery
from application import application
from src.mailers import *
import os

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=os.getenv('REDIS_URL')
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
def send_confirmation_email(recip_email, recip_token):
    ConfirmationMailer.send_message(recip_email, recip_token)

@celery.task(name='tasks.update_links')
def update_links():
    links_list = links.split(',')
    user_links = user.link_urls()
    actions = []

    new_links = np.setdiff1d(links_list,user_links)
    unsubed_links = np.setdiff1d(user_links,links_list)

    for link in new_links:
        link_ = Link.find_by_url(link)
        if link_ is None:
            try:
                response = subscription_attempt(link, user)
                actions.append(response)
            except:
                actions.append(f"Could not connect to {link}. All urls must be preceded by 'http://' or 'https://'.")

            continue

        us = UserSubscription(link_id=link_.id, user_id=user.id)
        db.session.add(us)
        db.session.commit()

    for link in unsubed_links:
        link_ = Link.find_by_url(link)
        us = UserSubscription.query.filter_by(link_id=link_.id, user_id=user.id).scalar()
        db.session.delete(us)
        db.session.commit()
        actions.append(f'Unsubscribed from {link}')

    return actions

@celery.task(name='tasks.update_user')
def update_user(user, form_data):
    update_links(user, form_data['links'])
    update_email(user, form_data['email'])[user.email == form_data['email']]
    update_filters(user, form_data['filters'])

@celery.task(name='tasks.update_email')
def update_email(user, new_email):
    return {
        False: user.update_email(new_email),
        True: do_nothing()
    }

@celery.task(name='tasks.update_filters')
def update_filters(user, filters):
    filters = filters.split(',')
    current_filters = user.filters()

    new_filters = np.setdiff1d(filters,current_filters)
    removed_filters = np.setdiff1d(current_filters,filters)

    for filter in new_filters:
        filter_ = Filter.find_by_word(filter)
        if filter_ is None:
            new_filter = Filter(word=filter)
            db.session.add(new_filter)
            db.session.commit()
            new_user_filter = UserFilter(user_id=user.id, filter_id=new_filter.id)
            db.session.add(new_user_filter)
            db.session.commit()
        else:
            new_user_filter = UserFilter(user_id=user.id, filter_id=filter_.id)
            db.session.add(new_user_filter)
            db.session.commit()

    for filter in removed_filters:
        filter_ = Filter.find_by_word(filter)
        user_filter = UserFilter.query.filter_by(user_id=user.id, filter_id=filter_.id).scalar()
        db.session.delete(user_filter)
        db.session.commit()
