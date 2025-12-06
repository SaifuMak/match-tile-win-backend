# serializers.py
from rest_framework import serializers
from .models import ConsolationPrize, Participant, Prize, PrizeResetLog
from django.utils.timezone import localtime
import pytz


class ParticipantSerializer(serializers.ModelSerializer):
    played_at = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d %b %Y %I:%M %p", read_only=True)
    # played_at = serializers.DateTimeField(format="%d %b %Y %I:%M %p", read_only=True)
    class Meta:
        model = Participant
        fields = "__all__"
    
    def get_played_at(self, obj):
        if obj.played_at:
            tz = pytz.timezone("Australia/Sydney")
            return localtime(obj.played_at, tz).strftime("%d %b %Y, %I:%M %p")
        return None
    
class PrizeDetailSerializer(serializers.ModelSerializer):
     class Meta:
         model = Prize
         fields = "__all__"

         
class ConsolationPrizeSerializer(serializers.ModelSerializer):
     class Meta:
         model = ConsolationPrize
         fields = "__all__"

class PrizeResetLogSerializer(serializers.ModelSerializer):
    recorded_at = serializers.DateTimeField(format="%d %b %Y %I:%M %p", read_only=True)
    class Meta:
        model = PrizeResetLog
        fields = "__all__"

    def get_recorded_at(self, obj):
        if obj.recorded_at:
            tz = pytz.timezone("Australia/Sydney")
            return localtime(obj.recorded_at, tz).strftime("%d %b %Y, %I:%M %p")
        return None
