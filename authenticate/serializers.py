from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, Serializer

from authenticate.models import User


class RegisterModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'fullname' , 'email' , 'password'
    def validate_email(self, value):
        query = User.objects.filter(email=value)
        if query.exists():
            raise ValidationError('Already exists email !')
        return value

    def validate_password(self, value):
        return make_password(value)

    def validate_fullname(self, value):
        if not value.replace(" ", "").isalpha():
            raise ValidationError("Fullname to'liq to'g'ri kiritilsin")
        return value

class VerifyOtpSerializer(Serializer):
    email = CharField(max_length=255)
    otp_code = CharField(max_length=255)







