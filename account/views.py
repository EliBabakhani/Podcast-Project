from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from API.serializer_user import UserSeriallizer


class RegisterView(APIView):
    def post(self, request):
        serializer=UserSeriallizer(date=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

