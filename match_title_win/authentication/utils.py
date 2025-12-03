from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.response import Response
from rest_framework import status


def perform_logout(request):
    refresh_token = request.COOKIES.get('session_persist')

    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            pass

    response = Response({'message': 'Logout successfull.'}, status=status.HTTP_200_OK)
    response.delete_cookie('session_id', samesite='None')
    response.delete_cookie('session_persist', samesite='None')
    return response