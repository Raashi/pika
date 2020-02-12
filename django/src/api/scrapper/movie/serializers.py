from rest_framework import serializers

from api.scrapper.serializers import BaseUploadSerializer, TMDB_image_fields, TMDB_video_fields, TMDB_review_fields
from api.scrapper.base.serializers import GenreUploadSerializer, CompanyUploadSerializer, KeywordUploadSerializer
from api.scrapper.person.serializers import PersonUploadSerializer

from pika.movie.models import Movie, Collection, MovieReleaseDate, MoviePoster, MovieBackdrop, MovieVideo, MovieReview, \
    MovieParticipation


class CollectionUploadSerializer(BaseUploadSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name', 'rus_name', 'poster', 'backdrop', 'overview', 'rus_overview']


class MovieReleaseDateUploadSerializer(BaseUploadSerializer):
    class Meta:
        model = MovieReleaseDate
        fields = ['movie', 'type', 'date', 'country']
        extra_kwargs = {
            'movie': {'required': False}
        }
        lookup_field = ['type', 'country']


class MoviePosterSerializer(BaseUploadSerializer):
    class Meta:
        model = MoviePoster
        fields = ['movie'] + TMDB_image_fields
        lookup_field = 'path'
        extra_kwargs = {'movie': {'required': False}}


class MovieBackdropSerializer(BaseUploadSerializer):
    class Meta:
        model = MovieBackdrop
        fields = ['movie'] + TMDB_image_fields
        lookup_field = 'path'
        extra_kwargs = {'movie': {'required': False}}


class MovieVideoSerializer(BaseUploadSerializer):
    class Meta:
        model = MovieVideo
        fields = ['movie'] + TMDB_video_fields
        lookup_field = 'tmdb_id'
        extra_kwargs = {'movie': {'required': False}}


class MovieReviewSerializer(BaseUploadSerializer):
    class Meta:
        model = MovieReview
        fields = ['movie'] + TMDB_review_fields
        lookup_field = 'tmdb_id'


class MovieParticipationSerializer(BaseUploadSerializer):
    person = PersonUploadSerializer(required=True, allow_null=False)

    class Meta:
        model = MovieParticipation
        fields = ['movie', 'person', 'job', 'character', 'rus_character', 'gender']

    def save(self, **kwargs):
        person = self.validated_data.pop('person').save()
        self.validated_data['person'] = person

        return super().save()


class MovieUploadSerializer(BaseUploadSerializer):
    collection = CollectionUploadSerializer(allow_null=True)
    genres = serializers.ListSerializer(child=GenreUploadSerializer)
    production_companies = serializers.ListSerializer(child=CompanyUploadSerializer)
    keywords = serializers.ListSerializer(child=KeywordUploadSerializer)

    releases = serializers.ListSerializer(child=MovieReleaseDateUploadSerializer)
    posters = serializers.ListSerializer(child=MoviePosterSerializer)
    backdrops = serializers.ListSerializer(child=MovieBackdropSerializer)
    videos = serializers.ListSerializer(child=MovieVideoSerializer)
    reviews = serializers.ListSerializer(child=MovieReviewSerializer)
    people = serializers.ListSerializer(child=MovieParticipationSerializer)

    class Meta:
        model = Movie
        fields = [
            'id', 'imdb_id', 'title', 'rus_title', 'overview', 'rus_overview', 'tagline', 'rus_tagline',
            'homepage', 'rus_homepage',
            'adult', 'budget', 'popularity', 'runtime', 'revenue', 'vote_average', 'vote_count', 'release_date',
            'status',
            'poster', 'backdrop', 'original_language', 'status', 'release_date',
            # complicated
            'collection', 'genres', 'production_companies', 'keywords'
            # these two use drf's common update implementation for many2many - every time it calls 'set'
            'production_countries', 'spoken_languages',
            # related
            'releases', 'posters', 'backdrops', 'videos', 'reviews', 'people'
        ]

    def save(self, **kwargs):
        # process Collection
        collection_serializer = self.validated_data.pop('collection')
        if collection_serializer is not None:
            collection = collection_serializer.save()
        else:
            collection = None
        self.validated_data['collection'] = collection

        # process Genres
        genre_serializers = self.validated_data.pop('genres')
        genres = [genre_serializer.save() for genre_serializer in genre_serializers]
        self.validated_data['genres'] = genres

        # process Companies
        company_serializers = self.validated_data.pop('production_companies')
        companies = [company_serializer.save() for company_serializer in company_serializers]
        self.validated_data['production_companies'] = companies

        # process keywords
        keyword_serializers = self.validated_data.pop('keywords')
        keywords = [keyword_serializer.save() for keyword_serializer in keyword_serializers]
        self.validated_data['keywords'] = keywords

        # production_countries and spoken_languages will process automatically

        release_serializers = self.validated_data.pop('releases')
        poster_serializers = self.validated_data.pop('posters')
        backdrop_serializers = self.validated_data.pop('backdrops')
        video_serializers = self.validated_data.pop('videos')
        review_serializers = self.validated_data.pop('reviews')
        people_serializers = self.validated_data.pop('people')

        # --------- create or update movie ---------------------

        movie: Movie = super().save(**kwargs)

        # save many2many fields
        movie.save()

        # process related objects
        self.updated_related(release_serializers, movie)
        self.updated_related(poster_serializers, movie)
        self.updated_related(backdrop_serializers, movie)
        self.updated_related(video_serializers, movie)
        self.updated_related(review_serializers, movie)
        self.updated_related(people_serializers, movie)

        return movie
