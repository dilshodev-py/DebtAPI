from http import HTTPStatus
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Q, Count
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView,UpdateAPIView
from rest_framework.views import APIView
from apps.models import Debt
from apps.serializers import ContactModelSerializer, DebtModelSerializer, DebtPutModelSerializer
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Contact
from .serializers import ContactUpdateSerializer
from rest_framework.exceptions import PermissionDenied


from rest_framework.response import Response
from rest_framework import status
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




@extend_schema(tags=["contact"])
class ContactUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = ContactUpdateSerializer
    permission_classes = IsAuthenticated,
    lookup_field = 'id'

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("Faqat o'zingizni kontaktlaringizni o'zgartira olasiz.")
        serializer.save()


@extend_schema(tags=["debt"])
class DebtPutApiView(UpdateAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtPutModelSerializer

class PayDebtView(APIView):
    def post(self, request, debt_id):
        debt = get_object_or_404(Debt, id=debt_id)

        if debt.is_paid:
            return Response({"xato": "Qarz allaqachon to‘langan"}, status=status.HTTP_400_BAD_REQUEST)
        debt.is_paid = True
        debt.save()

        return Response({"xato": "Qarz muvaffaqiyatli to‘landi"},status=status.HTTP_200_OK)



@extend_schema(tags=["debt"])
class DebtDestroyApiView(DestroyAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return super().get_queryset().filter(contact_id=self.request.user.id)

