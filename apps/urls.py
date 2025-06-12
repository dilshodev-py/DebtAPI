from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.views import HomeOverviewAPIView
from authenticate.views import RegisterAPIView, VerifyOtpAPIView, CustomTokenObtainPairView, CustomTokenRefreshView, \
    ForgotPasswordAPIView, ForgotPasswordOtpAPIView, ForgotChangePasswordAPIView

urlpatterns = [
    path('home/overview' , HomeOverviewAPIView.as_view()),
]
