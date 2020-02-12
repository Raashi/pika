from django.contrib import admin

from .models import Collection, Movie, MovieBackdrop, MoviePoster, MovieReleaseDate, MovieVideo, MovieParticipation, \
    MovieReview


class MovieBackdropAdmin(admin.TabularInline):
    model = MovieBackdrop


class MoviePosterAdmin(admin.TabularInline):
    model = MoviePoster


class MovieVideoAdmin(admin.TabularInline):
    model = MovieVideo


class MovieReleaseDateAdmin(admin.StackedInline):
    model = MovieReleaseDate


class MovieReviewAdmin(admin.StackedInline):
    model = MovieReview


class MovieParticipationAdmin(admin.StackedInline):
    model = MovieParticipation


class MovieAdmin(admin.ModelAdmin):
    inlines = [MovieBackdropAdmin, MoviePosterAdmin, MovieReleaseDateAdmin, MovieVideoAdmin, MovieReviewAdmin,
               MovieParticipationAdmin]


admin.site.register(Collection)
admin.site.register(Movie, MovieAdmin)
