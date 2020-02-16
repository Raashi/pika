from rest_framework import serializers

from api.scrapper.serializers import BaseUploadSerializer, TMDB_image_fields, TMDB_video_fields, TMDB_review_fields
from api.scrapper.base.serializers import GenreUploadSerializer, CompanyUploadSerializer, KeywordUploadSerializer
from api.scrapper.person.serializers import PersonUploadSerializer

from pika.movie.models import Movie, Collection, MovieReleaseDate, MoviePoster, MovieBackdrop, MovieVideo, \
    MovieReview, MovieParticipation


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
        lookup_fields = ['type', 'country']


class MoviePosterSerializer(BaseUploadSerializer):
    class Meta:
        model = MoviePoster
        fields = ['movie'] + TMDB_image_fields
        lookup_fields = ['path']
        extra_kwargs = {'movie': {'required': False}}


class MovieBackdropSerializer(BaseUploadSerializer):
    class Meta:
        model = MovieBackdrop
        fields = ['movie'] + TMDB_image_fields
        lookup_fields = ['path']
        extra_kwargs = {'movie': {'required': False}}


class MovieVideoSerializer(BaseUploadSerializer):
    class Meta:
        model = MovieVideo
        fields = ['movie'] + TMDB_video_fields
        lookup_fields = ['tmdb_id']
        extra_kwargs = {'movie': {'required': False}}


class MovieReviewSerializer(BaseUploadSerializer):
    class Meta:
        model = MovieReview
        fields = ['movie'] + TMDB_review_fields
        lookup_fields = ['tmdb_id']


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

    def save(self, return_fresh=False):
        # process Collection
        collection = self.validated_data.pop('collection')
        if collection is not None:
            collection = self.fields['collection'].save(validated_data=collection, instance=None)
        self.validated_data['collection'] = collection

        # process Genres
        self.validated_data['genres'] = self.save_arr_of_m2m(self.validated_data.pop('genres'), 'genres')

        # process Companies
        self.validated_data['production_companies'] = self.save_arr_of_m2m(
            self.validated_data.pop('production_companies'), 'production_companies'
        )

        # process keywords
        self.validated_data['keywords'] = self.save_arr_of_m2m(self.validated_data.pop('keywords'), 'keywords')

        # production_countries and spoken_languages will process automatically

        releases = self.validated_data.pop('releases')
        posters = self.validated_data.pop('posters')
        backdrops = self.validated_data.pop('backdrops')
        videos = self.validated_data.pop('videos')
        reviews = self.validated_data.pop('reviews')
        people = self.validated_data.pop('people')

        # --------- create or update movie ---------------------

        movie: Movie = super().save()

        # save many2many fields
        movie.save()

        # process related objects
        self.save_arr_of_related(releases, 'releases', 'movie', movie)
        self.save_arr_of_related(posters, 'posters', 'movie', movie)
        self.save_arr_of_related(backdrops, 'backdrops', 'movie', movie)
        self.save_arr_of_related(videos, 'videos', 'movie', movie)
        self.save_arr_of_related(reviews, 'reviews', 'movie', movie)
        self.save_arr_of_related(people, 'people', 'movie', movie)

        if return_fresh:
            movie.refresh_from_db()
        return movie
