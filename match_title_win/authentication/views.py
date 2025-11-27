from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import * 
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import authentication, exceptions
import jwt
from django.contrib.auth.hashers import check_password
from django.core.mail import EmailMessage
from django.core.mail import send_mail
import uuid
from .utils import clear_cookie
from django.views.decorators.csrf import csrf_exempt
from .models import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes

# Create your views here.

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        access_token = request.COOKIES.get('access_token')
        # print(access_token,'^^^^^^^^^^^^^^^ access')
        # print()
        # print(refresh_token,'^^^^^^^^^^^^^^^ refresh')
        
        if not access_token:
            if not refresh_token:
                raise AuthenticationFailed('No access token and refresh token not provided')
            return self.refresh_access_token(refresh_token)

        try:
            
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
            # print(payload,'^^^^^^^^^^^^^^^')

            user_id = payload['user_id']
            user = User.objects.get(id=user_id)
            return (user, None)

           
        except jwt.ExpiredSignatureError:
            if not refresh_token:
                raise AuthenticationFailed('Refresh token not provided')
            return self.refresh_access_token(refresh_token)

        except jwt.InvalidTokenError:
                raise AuthenticationFailed('Invalid refresh token')

        except User.DoesNotExist:
                raise AuthenticationFailed('User not found')

        
    def refresh_access_token(self, refresh_token):
        try:
            payload_refresh = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload_refresh['user_id']
            user = User.objects.get(id=user_id)

            # Generate a new access token
            refresh = RefreshToken.for_user(user)
            new_access_token = str(refresh.access_token)
            new_refresh_token = str(refresh)

            response = Response({'access_token': new_access_token}, status=status.HTTP_200_OK)
         
            response.set_cookie(
                key='access_token',
                value=new_access_token,
                httponly=True,
                secure=True,
                samesite='None',
                max_age=5*60  
            )


            response.set_cookie(
                key='refresh_token',
                value=new_refresh_token,
                httponly=True,
                secure=True,
                samesite='None',
                max_age=2*24*60 
            )

            # print("New tokens set in cookies")
            return (user, None)
            # return(response)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Refresh token has expired')

        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid refresh token')

        except User.DoesNotExist:
            raise AuthenticationFailed('User not found') 

class CheckLoginStatus(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
   
    def get(self, request):
        # print( request.user,'reached the protected  view ')
        return Response('success', status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def check_is_authenticated(request):
        return Response(' profile is verified ', status=status.HTTP_200_OK)

   