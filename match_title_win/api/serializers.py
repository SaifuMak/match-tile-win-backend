# serializers.py
from datetime import timedelta
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
    recorded_at = serializers.DateTimeField(format="%d %b", read_only=True)
    start_date = serializers.SerializerMethodField()

    class Meta:
        model = PrizeResetLog
        fields = "__all__"
        extra_fields = ['start_date']

    def get_recorded_at(self, obj):
        if obj.recorded_at:
            tz = pytz.timezone("Australia/Sydney")
            return localtime(obj.recorded_at, tz).strftime("%d %b")
        return None
    
    def get_start_date(self, obj):
        if obj.recorded_at:
            tz = pytz.timezone("Australia/Sydney")
            dt = localtime(obj.recorded_at, tz) - timedelta(days=7)
            return dt.strftime("%d %b")
        return None
