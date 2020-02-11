from django.db import models
from django.utils.translation import ugettext as _

from pika.db import models as pika_models


class Genre(pika_models.Model):
    id = pika_models.TMDBId()
    name = models.CharField(_('Genre name'), max_length=32)
    rus_name = models.CharField(_('Genre name in russian'), max_length=32, blank=True, null=True)

    class Meta:
        db_table = 'genre'
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')


class Collection(pika_models.Model):
    id = pika_models.TMDBId()
    name = models.CharField(_('Collection name'), max_length=64)
    rus_name = models.CharField(_('Collection name in russian'), max_length=64, blank=True, null=True)

    poster = pika_models.PosterImageField()
    backdrop = pika_models.BackdropImageField()

    overview = models.CharField(_('Overview'), max_length=256, blank=True, null=True)
    rus_overview = models.CharField(_('Overview in russian'), max_length=256, blank=True, null=True)


class Review(pika_models.Model):
    # we should still have id as AutoField to reduce db size
    tmdb_id = models.CharField(_('TMDB Id'), max_length=32, unique=True, db_index=True)
    author = models.CharField(_('Author'), max_length=64, blank=True, null=True)
    content = models.TextField(_('Text'))
    url = models.URLField(_('Review link'), blank=True, null=True)
    language = models.ForeignKey(to=pika_models.Language, on_delete=models.SET_NULL, related_name='reviews',
                                 verbose_name=_('Language'), blank=True, null=True)


MOVIE_STATUS_CHOICES = [
    (0, 'Rumored'),
    (1, 'Planned'),
    (2, 'In production'),
    (3, 'Post production'),
    (4, 'Released'),
    (5, 'Cancelled'),
]


class Movie(pika_models.Model):
    id = pika_models.TMDBId()
    imdb_id = pika_models.IMDBId()

    title = models.CharField(_('Title'), max_length=256)
    rus_title = models.CharField(_('Title in russian'), max_length=256, blank=True, null=True)

    overview = models.CharField(_('Overview'), max_length=256, blank=True, null=True)
    rus_overview = models.CharField(_('Overview in russian'), max_length=256, blank=True, null=True)

    tagline = models.CharField(_('Movie tagline'), max_length=128, blank=True, null=True)
    rus_tagline = models.CharField(_('Movie tagline in russian'), max_length=128, blank=True, null=True)

    homepage = models.URLField(_('Homepage'), blank=True, null=True)
    rus_homepage = models.URLField(_('Homepage for Russia'), blank=True, null=True)

    adult = models.BooleanField(_('Adult'))
    budget = models.IntegerField(_('Budget'), blank=True, null=True)
    popularity = models.DecimalField(_('Popularity'), decimal_places=2, max_digits=6)
    runtime = models.IntegerField(_('Movie runtime'), blank=True, null=True)
    revenue = models.IntegerField(_('Movie revenue'), blank=True, null=True)

    # marks
    vote_average = models.DecimalField(_('Vote average'), max_digits=4, decimal_places=2)
    vote_count = models.IntegerField(_('Vote count'))

    # keys
    collection = models.ForeignKey(to=Collection, on_delete=models.SET_NULL, related_name='movies',
                                   verbose_name=_('Collection'), blank=True, null=True)
    genres = models.ManyToManyField(to=Genre, related_name='movies', verbose_name=_('Genres'))
    original_language = models.ForeignKey(to=pika_models.Language, on_delete=models.SET_NULL, related_name='movies',
                                          verbose_name=_('Original language'), blank=True, null=True)
    production_companies = models.ManyToManyField(to=pika_models.Company, related_name='movies',
                                                  verbose_name=_('Production companies'))
    production_countries = models.ManyToManyField(to=pika_models.Country, related_name='movies',
                                                  verbose_name=_('Production countries'))
    spoken_languages = models.ManyToManyField(to=pika_models.Language, related_name='in_movies')
    keywords = models.ManyToManyField(to=pika_models.Keyword, related_name='movies')

    # world earliest release
    release_date = models.DateField(_('Release date'), blank=True, null=True)
    status = models.IntegerField(_('Status'), choices=MOVIE_STATUS_CHOICES)

    # images
    poster = pika_models.PosterImageField()
    backdrop = pika_models.BackdropImageField()

    #
    last_update = models.DateTimeField(_('Last update'), auto_now=True)


MOVIE_RELEASE_DATE_TYPE_CHOICES = [
    (1, 'Premiere'),
    (2, 'Theatrical (limited)'),
    (3, 'Theatrical'),
    (4, 'Digital'),
    (5, 'Physical'),
    (6, 'TV')
]


class MovieReleaseDate(pika_models.Model):
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE, related_name='release_dates')
    type = models.IntegerField(_('Release date type'), choices=MOVIE_RELEASE_DATE_TYPE_CHOICES)
    date = models.DateTimeField(_('Release date'))
    country = models.ForeignKey(to=pika_models.Country, on_delete=models.CASCADE, related_name='releases',
                                verbose_name=_('Release country'))


class MoviePoster(pika_models.TMDBImage):
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE, related_name='posters')

    class Meta:
        db_table = 'movie_posters'
        verbose_name = _('Movie poster')
        verbose_name_plural = _('Movie posters')
