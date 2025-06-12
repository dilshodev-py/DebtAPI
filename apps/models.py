from django.db import models

# Create your models here.

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import CharField, Model, ForeignKey, CASCADE
from django.db.models.fields import DecimalField, DateTimeField, BooleanField


class Contact(Model):
    user = ForeignKey('authenticate.User', on_delete=CASCADE)
    fullname = CharField(max_length=255)
    phone_number = CharField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)

class Debt(Model):
    contact = ForeignKey('apps.Contact', on_delete=CASCADE)
    debt_amount = DecimalField(max_digits=10, decimal_places=2)
    description = CharField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)
    due_date = DateTimeField()
    is_my_debt = BooleanField(default=False)
    is_paid = BooleanField(default=False)
    is_overdue = BooleanField(default=False)