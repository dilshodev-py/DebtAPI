from django.urls import path

from authenticate.views import RegisterAPIView , VerifyOtpAPIView

urlpatterns = [

    path('register' , RegisterAPIView.as_view()),
    path('register/verify/otp' , VerifyOtpAPIView.as_view())
]
