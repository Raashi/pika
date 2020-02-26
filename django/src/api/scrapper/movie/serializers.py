from api.scrapper.serializers import BaseUploadSerializer, TMDB_video_fields, TMDB_review_fields
from api.scrapper.base.serializers import JobField

from pika.movie.models import Movie, MovieReleaseDate, MovieVideo, \
    MovieReview, MovieParticipant


__all__ = ['MovieReleaseDateSerializer', 'MovieVideoSerializer', 'MovieReviewSerializer', 'MovieParticipantSerializer',
           'MovieSerializer', 'MovieExistsSerializer']


class MovieReleaseDateSerializer(BaseUploadSerializer):
    class Meta:
        model = MovieReleaseDate
        fields = ['movie', 'type', 'date', 'country', 'note']
        lookup_fields = ['type', 'country', 'movie', 'note']


class MovieVideoSerializer(BaseUploadSerializer):
    class Meta:
        model = MovieVideo
        fields = ['movie'] + TMDB_video_fields
        lookup_fields = ['tmdb_id']


class MovieReviewSerializer(BaseUploadSerializer):
    class Meta:
        model = MovieReview
        fields = ['movie'] + TMDB_review_fields
        lookup_fields = ['tmdb_id']


class MovieParticipantSerializer(BaseUploadSerializer):
    job = JobField(allow_null=True, required=False)

    class Meta:
        model = MovieParticipant
        fields = ['movie', 'tmdb_credit_id', 'person', 'job', 'character', 'rus_character']
        lookup_fields = ['tmdb_credit_id']


class MovieSerializer(BaseUploadSerializer):
    class Meta:
        model = Movie
        fields = [
            'id', 'imdb_id', 'title', 'rus_title', 'overview', 'rus_overview', 'tagline', 'rus_tagline',
            'homepage', 'rus_homepage',
            'adult', 'budget', 'popularity', 'runtime', 'revenue', 'vote_average', 'vote_count', 'release_date',
            'status',
            'poster', 'backdrop', 'original_language', 'collection',
            # m2m
            'genres', 'production_companies', 'keywords', 'production_countries', 'spoken_languages'
        ]


class MovieExistsSerializer(BaseUploadSerializer):
    class Meta:
        model = Movie
        fields = ['id']
