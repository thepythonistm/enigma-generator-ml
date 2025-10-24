from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .generator import generate_enigma
from .models import Riddle
from .serializers import RiddleSerializer

@api_view(['POST'])
def generate_enigma_view(request):
    try:
        level = request.data.get("level")
        print("LEVEL RECEIVED:", level)

        data = generate_enigma(level)
        print("DATA RETURNED FROM generate_enigma:", data)

        riddle_obj = Riddle.objects.create(
            riddle=data["riddle"],
            answer=data["answer"],
            difficulty=level
        )

        from .serializers import RiddleSerializer
        serializer = RiddleSerializer(riddle_obj)
        return Response(serializer.data)

    except Exception as e:
        import traceback
        print("🔥 FULL ERROR TRACEBACK:")
        traceback.print_exc()
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def get_answer_view(request, riddle_id):
    try:
        riddle = Riddle.objects.get(id=riddle_id)
        return Response({
            "id": riddle.id,
            "answer": riddle.answer
        })
    except Riddle.DoesNotExist:
        return Response({"error": "Riddle not found"}, status=404)
