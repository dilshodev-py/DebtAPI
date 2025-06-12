from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.views import HomeOverviewAPIView, ContactCreateApiView, ContactListApiView, ContactDebtListApiView, \
    DebtCreateApiView, ContactDestroyApiView
from authenticate.views import RegisterAPIView, VerifyOtpAPIView, CustomTokenObtainPairView, CustomTokenRefreshView, \
    ForgotPasswordAPIView, ForgotPasswordOtpAPIView, ForgotChangePasswordAPIView





urlpatterns = [
    path('home/overview' , HomeOverviewAPIView.as_view()),
    path('contact', ContactCreateApiView.as_view()),
    path("contact/list",ContactListApiView.as_view()),
    path("contact-debts/<int:pk>",ContactDebtListApiView.as_view()),
    path("contact-debt/<int:pk>",DebtCreateApiView.as_view()),
    path("contact/<int:pk>",ContactDestroyApiView.as_view()),


]
