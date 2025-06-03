from django.http import JsonResponse
from rest_framework.views import APIView

class HelloAPIVIEW(APIView):
    def get(self , request):
        return JsonResponse({"message" : "hello world"})
    