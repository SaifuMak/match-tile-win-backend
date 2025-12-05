from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ConsolationPrize, Participant, Prize
from rest_framework import status
from rest_framework.decorators import api_view
from .utils import draw_prize,check_and_reset_prizes, handle_consolation_prize
from django.db import transaction
from .serializers import ParticipantSerializer, PrizeDetailSerializer, PrizeDetailSerializer
from .pagination import GeneralListPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from authentication.views import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.db.models import F

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
            retailer=data.get("retailer"),
            amount_spent=data.get("amount_spent"),
            invoice=data.get("invoice")
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
        participant.has_played = True
        check_and_reset_prizes()
       
        if has_won:
                prize = draw_prize()
                participant.has_won = True

                if prize:
                    participant.reward = prize.amount if prize else 0
                else:
                    handle_consolation_prize()

                participant.save()
                return Response(
                            { "win_status": True, "reward": prize.amount if prize else 0},
                            status=status.HTTP_200_OK
                        )

        # If not won, give consolation prize if available   
        handle_consolation_prize()
       
        participant.save()  
        return Response(
            { "win_status": False,"reward": None},
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
    participants = Participant.objects.filter(has_played=True).order_by("-created_at")
    query = request.query_params.get("query")
    if query:
        participants = participants.filter(
            name__icontains=query
        )
    paginator = GeneralListPagination()
    paginated_participants = paginator.paginate_queryset(participants, request)
    serializer = ParticipantSerializer(paginated_participants, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def list_winners(request):
    print("Listing winners")
    winners = Participant.objects.filter(has_won=True).order_by("-created_at")
    query = request.query_params.get("query")
    if query:
        winners = winners.filter(
            name__icontains=query
        )
    paginator = GeneralListPagination()
    paginated_winners = paginator.paginate_queryset(winners, request)
    serializer = ParticipantSerializer(paginated_winners, many=True)
    return paginator.get_paginated_response(serializer.data)



@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def list_all_participants(request):
    participants = Participant.objects.filter(has_played=True).order_by("-created_at")
    serializer = ParticipantSerializer(participants, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def list_all_winners(request):
    winners = Participant.objects.filter(has_won=True).order_by("-created_at")
    serializer = ParticipantSerializer(winners, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PATCH"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def update_prize_claim_status(request, participant_id):
    try:
        participant = Participant.objects.get(id=participant_id)
        participant.is_prize_claimed = not participant.is_prize_claimed
        participant.save()
        return Response(
            {"message": "Prize claim status updated successfully."},
            status=status.HTTP_200_OK
        )
    except Participant.DoesNotExist:
        return Response(
            {"error": "Participant not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def rewards_details(request):
    vouchers = Prize.objects.all()
    consolation_prize = ConsolationPrize.objects.first()
    vouchers_serializer = PrizeDetailSerializer(vouchers, many=True)
    consolation_serializer = PrizeDetailSerializer(consolation_prize)
    data = {
        "vouchers": vouchers_serializer.data,
        "consolation": consolation_serializer.data,
    }

    return Response(data, status=status.HTTP_200_OK)