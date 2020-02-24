from celery import Celery
from celery.schedules import crontab


app = Celery('main', broker='amqp://admin:admin@rabbit:5672/grass')


app.conf.beat_schedule = {
    'tmdb-routine': {
        'task': 'sources.tmdb.tasks.routine',
        'schedule': crontab(hour=0, minute=0),
    },
}
