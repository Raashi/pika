from django.db import models
from django.utils.translation import ugettext as _

from .fields import *


class Model(models.Model):
    """base model class for future needs"""
    class Meta:
        abstract = True


class Language(Model):
    ISO_639_1_LENGTH = 2

    id = ISOField(_('ISO code'), max_length=ISO_639_1_LENGTH)
    # TODO: think of making name unique
    name = models.CharField(_('Language name'), max_length=32)
    rus_name = models.CharField(_('Language name in russian'), max_length=64, blank=True, null=True)

    class Meta:
        db_table = 'lang'
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')


class Country(Model):
    ISO_3166_1_LENGTH = 2

    id = ISOField(_('ISO country code'), max_length=ISO_3166_1_LENGTH)
    name = models.CharField(_('Country name'), max_length=128, unique=True, db_index=True)
    rus_name = models.CharField(_('Country name in russian'), max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'country'
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')


class TMDBImage(Model):
    path = models.CharField(_('Path'), max_length=32, unique=True, db_index=True)

    aspect_ratio = models.DecimalField(_('Aspect ratio'), max_digits=5, decimal_places=2, blank=True, null=True)
    width = models.IntegerField(_('Width'), default=-1)
    height = models.IntegerField(_('Height'), default=-1)

    vote_average = models.DecimalField(_('Vote average'), max_digits=4, decimal_places=2, blank=True, null=True)
    vote_count = models.IntegerField(_('Vote count'), default=0)

    class Meta:
        abstract = True


VIDEO_TYPE_CHOICES = [
    (0, 'Other'),
    (1, 'Trailer'),
    (2, 'Teaser'),
    (3, 'Clip'),
    (4, 'Featurette'),
    (5, 'Behind the Scenes'),
    (6, 'Bloopers'),
]


class TMDBVideo(Model):
    # + id
    tmdb_id = models.CharField(_('TMDB video id'), max_length=32, unique=True, db_index=True)
    language = models.ForeignKey(to=Language, on_delete=models.SET_NULL, related_name='videos', blank=True, null=True,
                                 verbose_name=_('Language'))
    country = models.ForeignKey(to=Country, on_delete=models.SET_NULL, related_name='videos', blank=True, null=True,
                                verbose_name=_('Country'))
    key = models.CharField(_('Key'), max_length=32, blank=True, null=True)
    name = models.CharField(_('Video name'), max_length=64, blank=True, null=True)

    size = models.IntegerField(_('Size'), default=-1)
    type = models.IntegerField(_('Type'), choices=VIDEO_TYPE_CHOICES, default=6)

    class Meta:
        abstract = True
