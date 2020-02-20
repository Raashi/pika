from django.contrib import admin

from .models import Collection, Movie, MovieReleaseDate, MovieVideo, MovieParticipant, \
    MovieReview


class MovieVideoAdmin(admin.TabularInline):
    model = MovieVideo


class MovieReleaseDateAdmin(admin.StackedInline):
    model = MovieReleaseDate


class MovieReviewAdmin(admin.StackedInline):
    model = MovieReview


class MovieParticipationAdmin(admin.StackedInline):
    model = MovieParticipant


class MovieAdmin(admin.ModelAdmin):
    inlines = [MovieReleaseDateAdmin, MovieVideoAdmin, MovieReviewAdmin, MovieParticipationAdmin]


admin.site.register(Collection)
admin.site.register(Movie, MovieAdmin)
