from celery import Celery


app = Celery('main', broker='amqp://admin:admin@rabbit:5672/grass')


@app.task
def add(x, y):
    return x + y
