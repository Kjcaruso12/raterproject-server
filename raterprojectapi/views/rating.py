"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from raterprojectapi.models.Game import Game
from raterprojectapi.models.Gamer import Gamer
from raterprojectapi.models.Rating import Rating

class RatingView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        rating = Rating.objects.get(pk=pk)
        serializer = RatingSerializer(rating)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        try:
            ratings = Rating.objects.all()
            game = request.query_params.get('game', None)
            if game is not None:
                ratings = ratings.filter(game_id=game)
            serializer = RatingSerializer(ratings, many=True)
            return Response(serializer.data)
        except Rating.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateRatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(gamer=gamer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        rating = Rating.objects.get(pk=pk)
        serializer = CreateRatingSerializer(rating, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        rating = Rating.objects.get(pk=pk)
        rating.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)



class RatingSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    # gamer = GamerSerializer(many=False)
    # gametype = GameTypeSerializer(many=False)
    class Meta:
        model = Rating
        fields = ('id', 'value', 'game', 'gamer')
        depth = 1

class CreateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'value', 'game']