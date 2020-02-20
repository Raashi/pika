from django.db import models
from django.utils.translation import ugettext as _

from pika.db import models as pika_models
from pika.base.models import DEPARTMENT_CHOICES, DEPARTMENT_MAX_LENGTH, Job


class Person(pika_models.Model):
    id = pika_models.TMDBId()
    imdb_id = pika_models.IMDBId()
    name = models.CharField(_('Person name'), max_length=64)
    rus_name = models.CharField(_('Person name in russian'), max_length=64, blank=True, null=True)
    gender = pika_models.GenderField()

    birthday = models.DateField(_('Birthday'), blank=True, null=True)
    deathday = models.DateField(_('Death day'), blank=True, null=True)

    known_for_department = models.CharField(_('Known for department'), max_length=DEPARTMENT_MAX_LENGTH,
                                            choices=DEPARTMENT_CHOICES, blank=True, null=True)

    # TODO: limit this correctly
    biography = models.CharField(_('Biography'), max_length=256, blank=True, null=True)
    rus_biography = models.CharField(_('Russian biography'), max_length=256, blank=True, null=True)

    popularity = models.DecimalField(_('Popularity'), decimal_places=2, max_digits=6, default='0.00')

    profile = pika_models.ProfileImageField()
    adult = models.BooleanField(_('Adult'), default=False)

    homepage = models.URLField(_('Homepage'), blank=True, null=True)

    class Meta:
        db_table = 'person'
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')


class Participation(pika_models.Model):
    tmdb_credit_id = models.CharField(_('TMDB credit ID'), max_length=32)
    person = models.ForeignKey(to=Person, on_delete=models.CASCADE, related_name='participants',
                               verbose_name=_('Person'))
    job = models.ForeignKey(to=Job, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Job'))

    character = models.CharField(_('Character'), max_length=64, blank=True, null=True)
    rus_character = models.CharField(_('Character in russian'), max_length=64, blank=True, null=True)
    character_gender = pika_models.GenderField()

    class Meta:
        abstract = True
