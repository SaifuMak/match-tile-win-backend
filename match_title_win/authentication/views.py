from urllib import request
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
from .utils import  perform_logout
from django.views.decorators.csrf import csrf_exempt
from .models import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes

# Create your views here.

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # refresh_token = request.COOKIES.get('refresh_token')
        # access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('session_persist')
        access_token = request.COOKIES.get('session_id')
        
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
        

@api_view(['POST'])
def login(request):
    print(request.data)
    try:
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
                email = serializer.validated_data['email']
                password = serializer.validated_data['password']
                user = authenticate(email=email, password=password)

                if user is None:

                    return Response({'error': 'Incorrect email or password'}, status=status.HTTP_401_UNAUTHORIZED)
               
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                response = Response({'message': 'Account Verified'}, status=status.HTTP_200_OK)

                response.set_cookie(
                    key='session_id',
                    value=access_token,
                    httponly=True,
                    secure=True,
                    samesite='None',
                    max_age= 5*60  
                )

                response.set_cookie(
                    key='session_persist',
                    value=refresh_token,
                    httponly=True,
                    secure=True,
                     samesite='None',
                    max_age= 1*24*60*60
                )

                return response
        else:   
                return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
            # Log the exception
            print(f'Error: {e}')
            return Response({'error': 'An unexpected error occurred. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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



    
@api_view(['POST'])
def user_logout(request):
    return perform_logout(request)