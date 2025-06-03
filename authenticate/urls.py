from django.urls import path

from authenticate.views import RegisterAPIView

urlpatterns = [

    path('register' , RegisterAPIView.as_view())
]
