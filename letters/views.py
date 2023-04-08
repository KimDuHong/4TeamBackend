from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Letter
from . import serializers


class Letters(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        letter = Letter.objects.filter(sender=request.user)
        serializer = serializers.LetterSerializer(letter)
        return Response(serializer.data)
