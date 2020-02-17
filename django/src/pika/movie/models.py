from django.db import models
from django.utils.translation import ugettext as _

from pika.db import models as pika_models
from pika.base.models import Genre, Company, Keyword, Job, Review, Collection
from pika.person.models import Person, Participation


MOVIE_STATUS_CHOICES = [
    (-1, 'Unknown'),
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

    adult = models.BooleanField(_('Adult'), default=False)
    budget = models.IntegerField(_('Budget'), blank=True, null=True)
    popularity = models.DecimalField(_('Popularity'), decimal_places=2, max_digits=6, blank=True, null=True)
    runtime = models.IntegerField(_('Movie runtime'), blank=True, null=True)
    revenue = models.IntegerField(_('Movie revenue'), blank=True, null=True)

    # marks
    vote_average = models.DecimalField(_('Vote average'), max_digits=4, decimal_places=2, blank=True, null=True)
    vote_count = models.IntegerField(_('Vote count'), default=0)

    # keys
    collection = models.ForeignKey(to=Collection, on_delete=models.SET_NULL, related_name='movies',
                                   verbose_name=_('Collection'), blank=True, null=True)
    genres = models.ManyToManyField(to=Genre, related_name='movies', verbose_name=_('Genres'), blank=True)
    original_language = models.ForeignKey(to=pika_models.Language, on_delete=models.SET_NULL, related_name='movies',
                                          verbose_name=_('Original language'), blank=True, null=True)
    production_companies = models.ManyToManyField(to=Company, related_name='movies',
                                                  verbose_name=_('Production companies'), blank=True)
    production_countries = models.ManyToManyField(to=pika_models.Country, related_name='movies',
                                                  verbose_name=_('Production countries'), blank=True)
    spoken_languages = models.ManyToManyField(to=pika_models.Language, related_name='in_movies', blank=True)
    keywords = models.ManyToManyField(to=Keyword, related_name='movies', blank=True)

    # world earliest release
    release_date = models.DateField(_('Release date'), blank=True, null=True)
    status = models.IntegerField(_('Status'), choices=MOVIE_STATUS_CHOICES, default=-1)

    # images
    poster = pika_models.PosterImageField()
    backdrop = pika_models.BackdropImageField()

    class Meta:
        db_table = 'movie'
        verbose_name = _('Movie')
        verbose_name_plural = _('Movies')


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

    class Meta:
        db_table = 'movie_release'
        verbose_name = _('Movie release')
        verbose_name_plural = _('Movie releases')


class MoviePoster(pika_models.TMDBImage):
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE, related_name='posters')

    class Meta:
        db_table = 'movie_poster'
        verbose_name = _('Movie poster')
        verbose_name_plural = _('Movie posters')


class MovieBackdrop(pika_models.TMDBImage):
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE, related_name='backdrops')

    class Meta:
        db_table = 'movie_backdrop'
        verbose_name = _('Movie backdrop')
        verbose_name_plural = _('Movie backdrops')


class MovieVideo(pika_models.TMDBVideo):
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE, related_name='videos')

    class Meta:
        db_table = 'movie_video'
        verbose_name = _('Movie video')
        verbose_name_plural = _('Movie videos')


class MovieParticipant(Participation):
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE, related_name='people',
                              verbose_name=_('Movie'))

    class Meta:
        db_table = 'movie_participant'
        verbose_name = 'Movie participant'
        verbose_name_plural = 'Movie participants'


class MovieReview(Review):
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE, related_name='reviews',
                              verbose_name=_('Movie'))

    class Meta:
        db_table = 'movie_review'
        verbose_name = _('Movie review')
        verbose_name_plural = _('Movie reviews')
