from django.db import models
from django.utils.translation import ugettext as _


__all__ = ['TMDBId', 'IMDBId', 'ISOField', 'LogoImageField', 'BackdropImageField', 'PosterImageField',
           'ProfileImageField', 'StillImageField']


class TMDBId(models.IntegerField):
    def __init__(self, verbose_name='', **kwargs):
        verbose_name = verbose_name if verbose_name != '' else _('TMDB Id')
        kwargs['primary_key'] = True
        super().__init__(verbose_name=verbose_name, **kwargs)


class IMDBId(models.CharField):
    IMDB_ID_LENGTH = 9

    def __init__(self, verbose_name='', **kwargs):
        verbose_name = verbose_name if verbose_name != '' else _('IMDB Id')
        kwargs['max_length'] = self.IMDB_ID_LENGTH
        kwargs['null'] = True
        kwargs['blank'] = True
        kwargs['unique'] = True
        kwargs['db_index'] = True
        super().__init__(verbose_name=verbose_name, **kwargs)


class ISOField(models.CharField):
    def __init__(self, verbose_name='', max_length=None, **kwargs):
        verbose_name = verbose_name if verbose_name != '' else _('ISO Code')
        kwargs['primary_key'] = True
        super().__init__(verbose_name=verbose_name, max_length=max_length, **kwargs)


class TMDBImageField(models.CharField):
    default_field_eng_name = ''

    def __init__(self, verbose_name='', **kwargs):
        verbose_name = verbose_name if verbose_name != '' else _(self.default_field_eng_name)
        kwargs['max_length'] = 64
        kwargs['blank'] = True
        kwargs['null'] = True
        super().__init__(verbose_name=verbose_name, **kwargs)


class LogoImageField(TMDBImageField):
    default_field_eng_name = 'Logo'


class BackdropImageField(TMDBImageField):
    default_field_eng_name = 'Backdrop'


class PosterImageField(TMDBImageField):
    default_field_eng_name = 'Poster'


class ProfileImageField(TMDBImageField):
    default_field_eng_name = 'Profile'


class StillImageField(TMDBImageField):
    default_field_eng_name = 'Still'
