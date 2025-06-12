from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authenticate.views import RegisterAPIView, VerifyOtpAPIView, CustomTokenObtainPairView, CustomTokenRefreshView, \
    ForgotPasswordAPIView, ForgotPasswordOtpAPIView, ForgotChangePasswordAPIView

urlpatterns = [
    path('register' , RegisterAPIView.as_view()),
    path('register/verify/otp' , VerifyOtpAPIView.as_view()),
    path('login', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('forgot-password', ForgotPasswordAPIView.as_view(), name='forgot'),
    path('forgot-password/otp', ForgotPasswordOtpAPIView.as_view(), name='forgot'),
    path('forgot/change-password', ForgotChangePasswordAPIView.as_view(), name='forgot'),
]
