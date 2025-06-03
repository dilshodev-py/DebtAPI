from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authenticate.views import RegisterAPIView, VerifyOtpAPIView, CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [

    path('register' , RegisterAPIView.as_view()),
    path('register/verify/otp' , VerifyOtpAPIView.as_view()),
    path('token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
