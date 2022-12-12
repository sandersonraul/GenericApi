from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from rest_framework import generics
from .models import User
import jwt, datetime
from django.http import HttpResponseNotFound
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

class RegisterView(APIView):
  def post(self, request):
    user = UserSerializer(data=request.data)
    user.is_valid(raise_exception=True)
    user.save()
    return Response(user.data)

class LoginView(APIView):
  def post(self, request):
    try:
      email = request.data['email']
      password = request.data['password']
    except:
      raise AuthenticationFailed('email and password are required')

    user = User.objects.filter(email=email).first()

    if user is None:
      raise AuthenticationFailed('User not found!')

    if not user.check_password(password):
      raise AuthenticationFailed('Incorrect password!')

    payload = {
      'id': user.id,
      'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
      'iat': datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

    response = Response()

    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {
      'jwt': token,
      'id': user.id
    }
    return response

class UserView(APIView):
  permission_classes = [IsAuthenticated,]
  authentication_classes = [SessionAuthentication,]
  def get(self, request, email):
    user = User.objects.filter(email=email).first()
    if user is None:
      return HttpResponseNotFound("User not founded")   
    serializer = UserSerializer(user)
    return Response(serializer.data)

class LogoutView(APIView):
  def post(self, request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
      'message': 'success'
    }
    return response

