from django.urls import path, include

urlpatterns = [
    path('scrapper/', include('api.scrapper.urls'))
]
