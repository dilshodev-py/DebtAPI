import json
import random
from datetime import timedelta

from django.contrib.auth.hashers import make_password
from redis import Redis
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, Serializer

from authenticate.models import User
from authenticate.tasks import send_email


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

class ForgotPasswordSerializer(Serializer):
    email = CharField(max_length=255)

    def validate_email(self, value):
        query = User.objects.filter(email=value)
        if not query.exists():
            raise ValidationError("User not found")
        random_code = random.randrange(10**5 , 10**6)
        send_email.delay(value , f"code : {random_code}")
        redis = Redis(decode_responses=True)
        data_str = json.dumps({"status" : False , "code" : random_code})
        redis.mset({value : data_str})
        redis.expire(value , time=timedelta(minutes=1))
        return value

class ForgotPasswordOtpSerializer(Serializer):
    email = CharField(max_length=255)
    otp_code = CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get('email')
        otp_code = attrs.get('otp_code')
        redis  =Redis(decode_responses=True)
        data_str = redis.mget(email)[0]
        if data_str:
            data_dict = json.loads(data_str)
        else:
            raise ValidationError("Expire time !")
        code = data_dict.get("code")
        if str(code) != str(otp_code):
            raise ValidationError("Tastqilash code xato !")
        data_str = json.dumps({"status": True})
        redis.mset({email : data_str})
        redis.expire(email , time=timedelta(minutes=2))
        return attrs


class ForgotChangePasswordSerializer(Serializer):
    email = CharField( max_length=255)
    password = CharField(max_length=90)
    confirm_password = CharField(max_length=90)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
        redis = Redis(decode_responses=True)
        data_str = redis.mget(email)[0]
        if not data_str:
            raise ValidationError("Emailni tastigidan o'ting")
        if password != confirm_password:
            raise ValidationError("Passwordni takrorlanishi xato ! Qayta uruning !")
        data_dict = json.loads(data_str)
        status = data_dict.get("status")
        if not status:
            raise ValidationError("Emailni tastiqlang")
        user = User.objects.filter(email=email).first()
        user.set_password(password)
        user.save()
        return attrs









