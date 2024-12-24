# HomeMate/server/app/tasks/celery.py

from celery import Celery
from celery.schedules import crontab
from flask import current_app
import pytz

celery = Celery("Application Jobs", include="app.tasks")

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from . import daily_rating_update, daily_reminder_professionals, monthly_report_customer
    sender.add_periodic_task(
        crontab(minute='0', hour='5'),
        daily_reminder_professionals.s(),
        name='daily_task'
    )

    sender.add_periodic_task(
        crontab(minute='0', hour='5'),
        daily_rating_update.s(),
        name='daily_task_2'
    )

    sender.add_periodic_task(
        crontab(minute='0', hour='5', day_of_month='1'),
        monthly_report_customer.s(),
        name='monthly_task'
    )

def init_celery(app):
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with current_app.app_context():
                return self.run(*args, **kwargs)
            
    celery.conf.update(broker_url=app.config["CELERY_BROKER_URL"], result_backend=app.config["CELERY_RESULT_BACKEND"])
    celery.Task = ContextTask
    app.app_context().push()

    celery.conf.timezone = 'Asia/Kolkata'

    return celery

