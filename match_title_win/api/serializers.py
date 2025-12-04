# serializers.py
from rest_framework import serializers
from .models import Participant
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