# serializers.py
from rest_framework import serializers
from .models import Participant


class ParticipantSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d %b %Y", read_only=True)
    played_at = serializers.DateTimeField(format="%d %b %Y", read_only=True)
    class Meta:
        model = Participant
        fields = "__all__"
