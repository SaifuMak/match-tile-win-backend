from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Participant
from rest_framework import status
from rest_framework.decorators import api_view
# Create your views here.


@api_view(['POST'])
def register_user(request):
    data = request.data

    try:
        player = Participant.objects.create(
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            city=data.get("city"),
        )

        return Response(
            {"user_id": player.id, "message": "User registered successfully"},
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )