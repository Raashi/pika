from copy import deepcopy

from rest_framework.reverse import reverse

from pika.db.models import Country, Language
from pika.base.models import Genre, Keyword, Company, Job
from pika.movie.models import Movie
from pika.person.models import Person

from testing.api.scrapper import ScrapperBaseTestCase
from testing.api.scrapper import templates


class CreateBasesMixin:
    @classmethod
    def create_bases(cls):
        cls.genre = Genre.objects.create(id=1, name='genre')
        cls.keyword = Keyword.objects.create(id=1, name='keyword')
        cls.company = Company.objects.create(id=1, name='company')
        cls.russia = Country.objects.create(id='RU', name='russia')
        cls.russian = Language.objects.create(id='ru', name='russian')


class MovieUploadTestCase(ScrapperBaseTestCase, CreateBasesMixin):
    url = reverse('scrapper:movies')
    example = {'items': [deepcopy(templates.movie)]}
    required_fields = {'id', 'title'}

    @classmethod
    def setUpTestData(cls):
        cls.create_bases()

        super().setUpTestData()

    def test_required_fields(self):
        response = self.post(self.url, {'items': [{}]}, expected_status=400).json()
        self.assertEqual(set(response[0]), self.required_fields)

    def test_upload(self):
        data = deepcopy(self.example)
        self.post(self.url, data, expected_status=204)

        self.assertEqual(Movie.objects.count(), 1)

        movie = Movie.objects.get(id=1)

        self.assertEqual(movie.genres.count(), 1)
        self.assertEqual(movie.keywords.count(), 1)
        self.assertEqual(movie.spoken_languages.count(), 1)
        self.assertEqual(movie.production_companies.count(), 1)

        data['items'][0]['genres'].append(2)
        data['items'][0]['keywords'].append(2)
        data['items'][0]['production_countries'].append('US')
        data['items'][0]['spoken_languages'].append('en')

        response = self.post(self.url, data, expected_status=400).json()
        self.assertEqual(set(response[0]), {'genres', 'keywords', 'production_countries', 'spoken_languages'})

        Genre.objects.create(id=2, name='2')
        response = self.post(self.url, data, expected_status=400).json()
        self.assertEqual(set(response[0]), {'keywords', 'production_countries', 'spoken_languages'})

        self.assertEqual(Movie.objects.count(), 1)


class UploadMovieRelatedTestCase(ScrapperBaseTestCase, CreateBasesMixin):
    url = reverse('scrapper:movies-relations')
    required_fields = {
        'releases': {'type', 'country', 'date', 'movie'},
        'posters': {'path', 'movie'},
        'backdrops': {'path', 'movie'},
        'videos': {'tmdb_id', 'movie'},
        'participants': {'person', 'movie'},
        'reviews': {'tmdb_id', 'movie'}
    }

    example = {
        'releases': [templates.get_template(templates.release)],
        'posters': [templates.get_image_template(movie=1)],
        'backdrops': [templates.get_image_template(movie=1)],
        'videos': [templates.get_video_template(movie=1)],
        'participants': [templates.get_template(templates.participant)],
        'reviews': [templates.get_template(templates.review, movie=1)]
    }

    @classmethod
    def setUpTestData(cls):
        cls.create_bases()

        cls.person = Person.objects.create(**templates.person)
        cls.job = Job.objects.create(**templates.job)

        movie_data = templates.get_template(templates.movie)
        for field in ['genres', 'production_companies', 'keywords', 'production_countries', 'spoken_languages']:
            movie_data.pop(field)
        movie_data['original_language'] = getattr(cls, 'russian')
        cls.movie = Movie.objects.create(**movie_data)

        super().setUpTestData()

    def test_required(self):
        self._test_inner_required_fields(self.url, self.required_fields)

    def test_upload(self):
        # also test lookups
        self.post(self.url, self.example, expected_status=204)
        self.post(self.url, self.example, expected_status=204)

        self.assertEqual(self.movie.release_dates.count(), 1)
        self.assertEqual(self.movie.posters.count(), 1)
        self.assertEqual(self.movie.backdrops.count(), 1)
        self.assertEqual(self.movie.videos.count(), 1)
        self.assertEqual(self.movie.participants.count(), 1)
        self.assertEqual(self.movie.reviews.count(), 1)



