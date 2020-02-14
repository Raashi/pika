from django.urls import path

from api import scrapper

app_name = 'scrapper'


urlpatterns = [
    path('login/', scrapper.LoginView.as_view(), name='login'),

    path('country/', scrapper.base.CountryUploadView.as_view(), name='country'),
    path('language/', scrapper.base.LanguageUploadView.as_view(), name='language'),
    path('person/', scrapper.person.PersonUploadView.as_view(), name='person')
]
