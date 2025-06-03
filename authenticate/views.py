import json
import random
from datetime import timedelta
from django.core.mail import send_mail
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from redis import Redis
from rest_framework.views import APIView
from authenticate.serializers import RegisterModelSerializer
from root.settings import EMAIL_HOST_USER



@extend_schema(tags=['auth'] , request=RegisterModelSerializer)
class RegisterAPIView(APIView):
    def post(self , request):
        data = request.data
        data_str = json.dumps(data)
        code = random.randint(10**5 , 10**6)
        email = data.get("email")
        send_mail("Verify Code" , f"Code: {code}" , EMAIL_HOST_USER , [email]) # TODO celery ishlatish kerak
        ser = RegisterModelSerializer(data=data)
        if ser.is_valid():
            redis = Redis(decode_responses=True)
            redis.mset({email: data_str})
            redis.expire(email , time=timedelta(minutes=1))
            return JsonResponse({"status": 200 , "message": "Emailga tastiqlash code yuborildi"})
