from django.urls import path

from authenticate.views import HelloAPIVIEW

urlpatterns = [
    path('hello' , HelloAPIVIEW.as_view())
]
