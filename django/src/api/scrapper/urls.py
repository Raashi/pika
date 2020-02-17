from django.urls import path

from api import scrapper

app_name = 'scrapper'


urlpatterns = [
    path('login/', scrapper.LoginView.as_view(), name='login'),

    path('countries/', scrapper.base.CountriesUploadView.as_view(), name='countries'),
    path('languages/', scrapper.base.LanguagesUploadView.as_view(), name='languages'),
    path('jobs/', scrapper.base.JobsUploadView.as_view(), name='jobs'),
    path('bases/', scrapper.base.BasesUploadView.as_view(), name='bases'),
    path('persons/', scrapper.person.PersonsUploadView.as_view(), name='persons'),
    path('persons/images', scrapper.person.PersonsImagesUploadView.as_view(), name='persons-images'),
    path('movies/', scrapper.movie.MoviesUploadView.as_view(), name='movies'),
    path('movies/relations/', scrapper.movie.MoviesRelationsUploadView.as_view(), name='movies-relations')
]
