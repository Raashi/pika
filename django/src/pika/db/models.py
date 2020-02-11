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
        db_table = 'county'
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')


class Keyword(Model):
    id = TMDBId()
    name = models.CharField(_('Keyword'), max_length=64)

    class Meta:
        db_table = 'keyword'
        verbose_name = _('Keyword')
        verbose_name_plural = _('Keywords')


DEPARTMENT_CHOICES = [
    ('Lighting', 'Lighting'),
    ('Crew', 'Crew'),
    ('Sound', 'Sound'),
    ('Actors', 'Actors'),
    ('Directing', 'Directing'),
    ('Visual Effects', 'Visual Effects'),
    ('Writing', 'Writing'),
    ('Camera', 'Camera'),
    ('Costume & Make-Up', 'Costume & Make-Up'),
    ('Editing', 'Editing'),
    ('Art', 'Art'),
    ('Production', 'Production'),
]

DEPARTMENT_MAX_LENGTH = 20


class Job(Model):
    # name is unique, but we still have and id as AutoField
    department = models.CharField(_('Department name'), max_length=DEPARTMENT_MAX_LENGTH, choices=DEPARTMENT_CHOICES)
    name = models.CharField(_('Job name'), max_length=64, unique=True, db_index=True)
    rus_name = models.CharField(_('Job name in russian'), max_length=64, blank=True, null=True)

    class Meta:
        db_table = 'job'
        verbose_name = _('Job')
        verbose_name_plural = _('Jobs')

    @staticmethod
    def get_by_name(name):
        return Job.objects.get(name=name)


class Company(Model):
    id = TMDBId()

    name = models.CharField(_('Company name'), max_length=128)
    rus_name = models.CharField(_('Company name in russian'), max_length=128, blank=True, null=True)

    description = models.CharField(_('Company description'), max_length=256, blank=True, null=True)
    rus_description = models.CharField(_('Company description in russian'), max_length=256, blank=True, null=True)

    headquarters = models.CharField(_('Headquarters'), max_length=256, blank=True, null=True)
    homepage = models.URLField(_('Homepage'), blank=True, null=True)

    origin_country = models.ForeignKey(verbose_name=_('Origin country'), to=Country, on_delete=models.SET_NULL,
                                       blank=True, null=True, related_name='companies', to_field='iso_3166_1')

    parent_company = models.ForeignKey(verbose_name=_('Parent company'), to='self',  on_delete=models.SET_NULL,
                                       blank=True, null=True, to_field='id')

    logo = LogoImageField(_('Company logo'))

    class Meta:
        db_table = 'company'
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')


class TMDBImage(Model):
    path = models.CharField(_('Path'), max_length=64)

    aspect_ratio = models.DecimalField(_('Aspect ratio'), max_digits=5, decimal_places=2)
    width = models.IntegerField(_('Width'))
    height = models.IntegerField(_('Height'))

    vote_average = models.IntegerField(_('Vote average'))
    vote_count = models.IntegerField(_('Vote count'))

    class Meta:
        abstract = True
