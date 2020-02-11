from django.db import models
from django.utils.translation import ugettext as _

from pika.db import models as pika_models
from pika.movie.models import Movie

GENDER_CHOICES = [
    (0, 'unknown'),
    (1, 'Female'),
    (2, 'Male'),
]


class Person(pika_models.Model):
    id = pika_models.TMDBId()
    imdb_id = pika_models.IMDBId()
    name = models.CharField(_('Person name'), max_length=64)
    rus_name = models.CharField(_('Person name in russian'), max_length=64, blank=True, null=True)
    gender = models.IntegerField(_('Gender'), choices=GENDER_CHOICES)

    birthday = models.DateField(_('Birthday'), blank=True, null=True)
    deathday = models.DateField(_('Death day'), blank=True, null=True)

    known_for_department = models.CharField(_('Known for department'), max_length=pika_models.DEPARTMENT_MAX_LENGTH,
                                            choices=pika_models.DEPARTMENT_CHOICES, blank=True, null=True)

    # TODO: limit this correctly
    biography = models.CharField(_('Biography'), max_length=256, blank=True, null=True)
    rus_biography = models.CharField(_('Russian biography'), max_length=256, blank=True, null=True)

    popularity = models.DecimalField(_('Popularity'), decimal_places=2, max_digits=6)

    profile = pika_models.ProfileImageField()
    adult = models.BooleanField(_('Adult'))

    homepage = models.URLField(_('Homepage'), blank=True, null=True)

    class Meta:
        db_table = 'person'
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')


class Participation(pika_models.Model):
    person = models.ForeignKey(to=Person, on_delete=models.CASCADE, related_name='participations',
                               verbose_name=_('Person'))
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE, related_name='people',
                              verbose_name=_('Movie'))
    job = models.ForeignKey(to=pika_models.Job, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Job'))

    character = models.CharField(_('Character'), max_length=64, blank=True, null=True)
    rus_character = models.CharField(_('Character in russian'), max_length=64, blank=True, null=True)

    class Meta:
        db_table = 'participation'
        verbose_name = 'Participation'
        verbose_name_plural = 'Participation'


class PersonTMDBImage(pika_models.TMDBImage):
    person = models.ForeignKey(to=Person, on_delete=models.CASCADE, related_name='images',
                               verbose_name=_('Person'))

    class Meta:
        db_table = 'person_images'
        verbose_name = _('Person image')
        verbose_name_plural = _('Person images')
