import os
import jwt
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import generics
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from app.auth.serializers import RegistrationSerializer, UserLoginSerializer, LogoutSerializer
from app.models import User

from app.auth.serializers import RegistrationSerializer, UserLoginSerializer, LogoutSerializer
from app.models import User

# Create your views here.

class RegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token

        current_sites = get_current_site(request).domain
        status_code = status.HTTP_201_CREATED
        response = {
            'Success': 'True',
            'StatusCode': status_code,
            'UserEmail': serializer.data['email'],
            'Message': 'Registered successfully',
        }

        return Response(response, status=status_code)
    

class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        get_user = User.objects.get(email=serializer.data['email'])
        get_user.save()

        if valid:
            status_code = status.HTTP_200_OK
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'email': serializer.data['email'],
                'first_name': serializer.data['first_name'],
                'last_name': serializer.data['last_name'],
                'user_id': get_user.id
            }
            return Response(response, status=status_code)

class LogoutAPIView(generics.GenericAPIView):

    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)