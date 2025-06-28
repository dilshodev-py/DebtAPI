from django.urls import path

from apps.views import HomeOverviewAPIView, ContactCreateApiView, ContactListApiView, ContactDebtListApiView, \
    DebtCreateApiView, ContactDestroyApiView, DebtListApiView, DebtPutApiView, DebtDestroyApiView, ContactUpdateAPIView, \
    PayDebtView

urlpatterns = [
    path('home/overview' , HomeOverviewAPIView.as_view()),
    path('contact', ContactCreateApiView.as_view()),
    path("contact/list",ContactListApiView.as_view()),
    path("contact-debts/<int:pk>",ContactDebtListApiView.as_view()),
    path("contact-debt/<int:pk>",DebtCreateApiView.as_view()),
    path("debt/list",DebtListApiView.as_view()),
    path("contact/<int:pk>",ContactDestroyApiView.as_view()),
    path("debt/put/<int:pk>", DebtPutApiView.as_view()),
    path("debt/delete/<int:pk>/", DebtDestroyApiView.as_view()),
    path("contact/update/<int:id>",ContactUpdateAPIView.as_view()),
    path('debts/paid/<int:debt_id>',PayDebtView.as_view()),
]