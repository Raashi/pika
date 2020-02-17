from api.scrapper.serializers import BaseUploadSerializer, TMDB_image_fields, TMDB_video_fields, TMDB_review_fields

from pika.movie.models import Movie, MovieReleaseDate, MoviePoster, MovieBackdrop, MovieVideo, \
    MovieReview, MovieParticipant


__all__ = ['MovieReleaseDateSerializer', 'MoviePosterSerializer', 'MovieBackdropSerializer', 'MovieVideoSerializer',
           'MovieReviewSerializer', 'MovieParticipantSerializer', 'MovieSerializer']


class MovieReleaseDateSerializer(BaseUploadSerializer):
    class Meta:
        model = MovieReleaseDate
        fields = ['movie', 'type', 'date', 'country']
        lookup_fields = ['type', 'country']


class MoviePosterSerializer(BaseUploadSerializer):
    class Meta:
        model = MoviePoster
        fields = ['movie'] + TMDB_image_fields
        lookup_fields = ['path']


class MovieBackdropSerializer(BaseUploadSerializer):
    class Meta:
        model = MovieBackdrop
        fields = ['movie'] + TMDB_image_fields
        lookup_fields = ['path']


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
    class Meta:
        model = MovieParticipant
        fields = ['movie', 'person', 'job', 'character', 'rus_character', 'gender']
        extra_kwargs = {'movie': {'required': False}}
        lookup_fields = ['movie', 'person']


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
