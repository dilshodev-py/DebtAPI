import json
import random
from datetime import timedelta
from http import HTTPStatus

from django.core.mail import send_mail
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from redis import Redis
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authenticate.serializers import RegisterModelSerializer, VerifyOtpSerializer, ForgotPasswordSerializer, \
    ForgotPasswordOtpSerializer, ForgotChangePasswordSerializer
from authenticate.tasks import send_email
from root.settings import EMAIL_HOST_USER


@extend_schema(tags=['auth'], request=RegisterModelSerializer)
class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data
        code = random.randint(10 ** 5, 10 ** 6)
        data['code'] = code
        data_str = json.dumps(data)
        email = data.get("email")
        # send_mail("Verify Code" , f"Code: {code}" , EMAIL_HOST_USER , [email]) # TODO celery ishlatish kerak
        # send_email(email, f"Code: {code}")
        ser = RegisterModelSerializer(data=data)
        if ser.is_valid():
            redis = Redis(decode_responses=True)
            redis.mset({email: data_str})
            redis.expire(email, time=timedelta(minutes=1))
            return JsonResponse({"status": 200, "message": "Emailga tastiqlash code yuborildi","code": code})
        return JsonResponse({"status": HTTPStatus.BAD_REQUEST, "errors": ser.errors })


@extend_schema(tags=['auth'], request=VerifyOtpSerializer)
class VerifyOtpAPIView(APIView):
    serializer_class = VerifyOtpSerializer
    def post(self, request):
        data = request.data
        email = data.get("email")
        otp_code = data.get("otp_code")
        r = Redis(decode_responses=True)
        data_str = r.mget(email)[0]
        if not data_str:
            return JsonResponse({"status": 400, "error": "tastiqlash vaqti tugadi !"})
        data_dict = json.loads(data_str)
        code = data_dict.pop("code")
        if str(code) != str(otp_code):
            return JsonResponse({"status": 400, "error": "Tastiqlash code xato !"})
        serializer = RegisterModelSerializer(data=data_dict)
        if serializer.is_valid():
            serializer.save()
        else:
            return JsonResponse({"status": 400, "error": serializer.errors})
        return JsonResponse({"status": 201, "message": "Mofaqiyatli register qilindi !"})





@extend_schema(tags=['auth'])
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(tags=['auth'])
class CustomTokenRefreshView(TokenRefreshView):
    pass

@extend_schema(tags=['auth'] , request=ForgotPasswordSerializer)
class ForgotPasswordAPIView(APIView):
    def post(self , request):
        data = request.data
        serializer = ForgotPasswordSerializer(data=data)
        if serializer.is_valid():
            return JsonResponse({"status" : HTTPStatus.OK , 'message': "Emailga tastiqlash code yuborildi !"})
        return JsonResponse({"status" : HTTPStatus.BAD_REQUEST , 'errors': serializer.errors})

@extend_schema(tags=['auth'], request=ForgotPasswordOtpSerializer)
class ForgotPasswordOtpAPIView(APIView):
    def post(self, request):
        data = request.data
        serializer = ForgotPasswordOtpSerializer(data=data)
        if serializer.is_valid():
            return JsonResponse({"status": HTTPStatus.OK , "message": "Mofaqiyatli tastiqlandi"})
        return JsonResponse({"status" : HTTPStatus.BAD_REQUEST , "errors": serializer.errors})

@extend_schema(tags=['auth'] , request=ForgotChangePasswordSerializer)
class ForgotChangePasswordAPIView(APIView):
    def post(self , request):
        data = request.data
        serializer = ForgotChangePasswordSerializer(data=data)
        if serializer.is_valid():
            return JsonResponse({"status" : HTTPStatus.ACCEPTED , 'message': "Password o'zgartirildi"})
        return JsonResponse({"status" : HTTPStatus.BAD_REQUEST , 'errors': serializer.errors})








