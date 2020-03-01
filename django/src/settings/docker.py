from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pika',
        'USER': 'pika',
        'PASSWORD': 'pika',
        'HOST': 'db',
        'PORT': 5432,
    }
}
