from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Participant
from rest_framework import status
from rest_framework.decorators import api_view
from .utils import draw_prize
from django.db import transaction
from .serializers import ParticipantSerializer
from .pagination import GeneralListPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from authentication.views import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
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
    

@api_view(['POST'])
@transaction.atomic
def get_my_rewards(request):
    id = request.data.get("id")
    has_won = request.data.get("has_won")
    time = request.data.get("time")

    try:
        participant = Participant.objects.get(id=id)
        participant.time_taken = time
       
        if has_won:
                 participant.has_won = True
                 participant.save()
                 return Response(
                        { "win_status": True, "reward": None},
                        status=status.HTTP_200_OK
                    )
        prize = draw_prize()
        
        participant.reward = prize.amount if prize else 0
        participant.save()  
        return Response(
            { "win_status": False,"reward": participant.reward},
            status=status.HTTP_200_OK
        )

    except Participant.DoesNotExist:
        return Response(
            {"error": "Participant not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def list_participants(request):
    print("Listing participants")
    participants = Participant.objects.all().order_by("-created_at")
    paginator = GeneralListPagination()
    paginated_participants = paginator.paginate_queryset(participants, request)
    serializer = ParticipantSerializer(paginated_participants, many=True)
    return paginator.get_paginated_response(serializer.data)