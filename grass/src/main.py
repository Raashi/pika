import sys
import startup

from celery import Celery
from celery.schedules import crontab

app = Celery('main', broker='amqp://admin:admin@localhost:5672/grass', include=['sources.tmdb.tasks'])


app.conf.beat_schedule = {
    'tmdb-routine': {
        'task': 'sources.tmdb.tasks.routine',
        'schedule': crontab(hour=0, minute=0),
    },
}

if sys.argv[1] == 'startup':
    import time

    startup.startup(app)

    while True:
        time.sleep(30)
