"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from raterprojectapi.models.Gamer import Gamer

class GamerView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        gamer = Gamer.objects.get(pk=pk)
        serializer = GamerSerializer(gamer)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        try:
            gamers = Gamer.objects.all()
            user = request.query_params.get('user', None)
            if user is not None:
                gamers = gamers.filter(user_id=user)
            serializer = GamerSerializer(gamers, many=True)
            return Response(serializer.data)
        except Gamer.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class GamerSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """

    class Meta:
        model = Gamer
        fields = ('id', 'bio', 'user')
        depth = 1

