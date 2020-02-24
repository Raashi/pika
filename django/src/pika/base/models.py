from django.db import models
from django.utils.translation import ugettext as _

from pika.db import models as pika_models


class Keyword(pika_models.Model):
    id = pika_models.TMDBId()
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


class Job(pika_models.Model):
    # plus id as AutoField
    department = models.CharField(_('Department name'), max_length=DEPARTMENT_MAX_LENGTH, choices=DEPARTMENT_CHOICES)
    name = models.CharField(_('Job name'), max_length=128)
    rus_name = models.CharField(_('Job name in russian'), max_length=64, blank=True, null=True)

    class Meta:
        db_table = 'job'
        verbose_name = _('Job')
        verbose_name_plural = _('Jobs')

    @staticmethod
    def get_by_name(name):
        return Job.objects.get(name=name)


class Company(pika_models.Model):
    id = pika_models.TMDBId()

    name = models.CharField(_('Company name'), max_length=128)
    rus_name = models.CharField(_('Company name in russian'), max_length=128, blank=True, null=True)

    description = models.CharField(_('Company description'), max_length=256, blank=True, null=True)
    rus_description = models.CharField(_('Company description in russian'), max_length=256, blank=True, null=True)

    headquarters = models.CharField(_('Headquarters'), max_length=256, blank=True, null=True)
    homepage = models.URLField(_('Homepage'), blank=True, null=True)

    origin_country = models.ForeignKey(verbose_name=_('Origin country'), to=pika_models.Country,
                                       on_delete=models.SET_NULL, blank=True, null=True, related_name='companies')

    parent_company = models.ForeignKey(verbose_name=_('Parent company'), to='self',  on_delete=models.SET_NULL,
                                       blank=True, null=True)

    logo = pika_models.LogoImageField(_('Company logo'))

    class Meta:
        db_table = 'company'
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')


class Genre(pika_models.Model):
    id = pika_models.TMDBId()
    name = models.CharField(_('Genre name'), max_length=32)
    rus_name = models.CharField(_('Genre name in russian'), max_length=32, blank=True, null=True)

    class Meta:
        db_table = 'genre'
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')


class Review(pika_models.Model):
    # we should still have id as AutoField to reduce db size
    tmdb_id = models.CharField(_('TMDB Id'), max_length=32, unique=True, db_index=True)
    author = models.CharField(_('Author'), max_length=64, blank=True, null=True)
    content = models.TextField(_('Text'), default='')
    url = models.URLField(_('Review link'), blank=True, null=True)
    language = models.ForeignKey(to=pika_models.Language, on_delete=models.SET_NULL, related_name='reviews',
                                 verbose_name=_('Language'), blank=True, null=True)

    class Meta:
        abstract = True


class Collection(pika_models.Model):
    id = pika_models.TMDBId()
    name = models.CharField(_('Collection name'), max_length=128)
    rus_name = models.CharField(_('Collection name in russian'), max_length=64, blank=True, null=True)

    poster = pika_models.PosterImageField()
    backdrop = pika_models.BackdropImageField()

    class Meta:
        db_table = 'collection'
        verbose_name = _('Collection')
        verbose_name_plural = _('Collections')
