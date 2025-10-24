from rest_framework import serializers
from .models import Riddle

class RiddleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Riddle
        fields = ['id', 'riddle', 'difficulty', 'created_at']
