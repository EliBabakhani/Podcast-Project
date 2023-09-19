from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from API.serializer_user import UserSeriallizer
import jwt
import datetime
from .models import User


class RegisterView(APIView):
    def post(self, request):
        serializer=UserSeriallizer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        email=request.data['email']
        password=request.data['password']
        user=User.objects.filter(email=email).first()
        if user:
            if user.check_password(password):
                payload={
                    'id':user.id,
                    'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
                    'iat':datetime.datetime.utcnow()
                    }
                token = jwt.encode(payload, 'secret','HS256')
                response=Response()
                response.set_cookie(key='jwt', value=token, httponly=True)
                response.data={'jwt':token}
                return response
            raise AuthenticationFailed('Incorrect password!')
        raise AuthenticationFailed('User not found')