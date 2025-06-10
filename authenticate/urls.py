from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authenticate.views import RegisterAPIView, VerifyOtpAPIView, CustomTokenObtainPairView, CustomTokenRefreshView, \
    ForgotPasswordAPIView, ForgotPasswordOtpAPIView, ForgotChangePasswordAPIView

urlpatterns = [
    path('auth/register' , RegisterAPIView.as_view()),
    path('auth/register/verify/otp' , VerifyOtpAPIView.as_view()),
    path('auth/login', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/forgot-password', ForgotPasswordAPIView.as_view(), name='forgot'),
    path('auth/forgot-password/otp', ForgotPasswordOtpAPIView.as_view(), name='forgot'),
    path('auth/forgot/change-password', ForgotChangePasswordAPIView.as_view(), name='forgot'),
]
