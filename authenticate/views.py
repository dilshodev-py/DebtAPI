import json
import random
from datetime import timedelta
from django.core.mail import send_mail
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from redis import Redis
from rest_framework.views import APIView

from authenticate.models import User
from authenticate.serializers import RegisterModelSerializer, VerifyOtpSerializer
from root.settings import EMAIL_HOST_USER



@extend_schema(tags=['auth'] , request=RegisterModelSerializer)
class RegisterAPIView(APIView):
    def post(self , request):
        data = request.data
        code = random.randint(10**5 , 10**6)
        data['code'] = code
        data_str = json.dumps(data)
        email = data.get("email")
        send_mail("Verify Code" , f"Code: {code}" , EMAIL_HOST_USER , [email]) # TODO celery ishlatish kerak
        ser = RegisterModelSerializer(data=data)
        if ser.is_valid():
            redis = Redis(decode_responses=True)
            redis.mset({email: data_str})
            redis.expire(email , time=timedelta(minutes=1))
            return JsonResponse({"status": 200 , "message": "Emailga tastiqlash code yuborildi"})

@extend_schema(tags=['auth'] , request=VerifyOtpSerializer)
class VerifyOtpAPIView(APIView):
    def post(self, request):
        data=  request.data
        email = data.get("email")
        otp_code = data.get("otp_code")
        r = Redis(decode_responses=True)
        data_str = r.mget(email)
        if not data_str:
            return JsonResponse({"status": 400 , "message": "tastiqlash vaqti tugadi !"})
        data_dict = json.loads(data_str)
        code = data_dict.pop("code")
        if str(code) != str(otp_code):
            return JsonResponse({"status": 400 , "message": "Tastiqlash code xato !"})
        User.objects.create(**data_dict)
        return JsonResponse({"status": 201, "message": "Mofaqiyatli register qilindi !"})





