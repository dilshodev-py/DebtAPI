from email.policy import default
from http import HTTPStatus

from django.db.models import Sum, Q, Count
from django.http import JsonResponse
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from apps.models import Debt, Contact
from apps.serializers import ContactModelSerializer, DebtModelSerializer


# Create your views here.

class HomeOverviewAPIView(APIView):
    permission_classes = IsAuthenticated,

    def get(self, request):
        data = request.data
        user = request.user

        user_debts = Debt.objects.filter(contact__user=user)

        my_debt = user_debts.aggregate(
            my_debt=Sum('debt_amount', filter=Q(is_my_debt=True, is_paid=False, is_overdue=False), default=0),
            their_debt=Sum('debt_amount', filter=Q(is_my_debt=False, is_paid=False, is_overdue=False), default=0),
            expired_debt=Sum('debt_amount', filter=Q(is_paid=False, is_overdue=True), default=0),
            overdue=Count('id', filter=Q(is_paid=False, is_overdue=True), distinct=True)
        )

        return JsonResponse({"status": HTTPStatus.OK, "data": my_debt})
@extend_schema(tags=["contact"])
class ContactCreateApiView(CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactModelSerializer
    permission_classes = IsAuthenticated,



@extend_schema(tags=["contact"])
class ContactListApiView(ListAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactModelSerializer
    permission_classes = IsAuthenticated,

    def get_queryset(self):
        query = super().get_queryset().filter(user=self.request.user)
        return query

@extend_schema(tags=["debt"])
class ContactDebtListApiView(ListAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtModelSerializer
    permission_classes = IsAuthenticated,

    def get_queryset(self):
        contact_pk = self.kwargs.get("pk")
        query = super().get_queryset().filter(contact__user=self.request.user,contact_id = contact_pk)
        return query


@extend_schema(tags=["debt"])
class ContactDebtListApiView(ListAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtModelSerializer
    permission_classes = IsAuthenticated,

    def get_queryset(self):
        contact_pk = self.kwargs.get("pk")
        query = super().get_queryset().filter(contact__user=self.request.user)
        if contact_pk:
            query = query.filter(contact_id = contact_pk)
        return query

@extend_schema(tags=["debt"])
class DebtListApiView(ListAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtModelSerializer
    permission_classes = IsAuthenticated,

    def get_queryset(self):
        contact_pk = self.kwargs.get("pk")
        query = super().get_queryset().filter(contact__user=self.request.user)
        return query


@extend_schema(tags=["debt"])
class DebtCreateApiView(CreateAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtModelSerializer
    permission_classes = IsAuthenticated,

@extend_schema(tags=["contact"])
class ContactDestroyApiView(DestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactModelSerializer
    permission_classes = IsAuthenticated,



