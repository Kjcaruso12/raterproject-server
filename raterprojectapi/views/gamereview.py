"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from raterprojectapi.models.Game import Game
from raterprojectapi.models.Gamer import Gamer
from raterprojectapi.models.Review import Review

class ReviewView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single review

        Returns:
            Response -- JSON serialized review
        """
        review = Review.objects.get(pk=pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all reviews

        Returns:
            Response -- JSON serialized list of review
        """
        try:
            reviews = Review.objects.all()
            game = request.query_params.get('game', None)
            if game is not None:
                reviews = reviews.filter(game_id=game)

            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data)
        except Review.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized review instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(gamer=gamer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        review = Game.objects.get(pk=pk)
        serializer = CreateReviewSerializer(review, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        review = Review.objects.get(pk=pk)
        review.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)



class ReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    # gamer = GamerSerializer(many=False)
    # gametype = GameTypeSerializer(many=False)
    class Meta:
        model = Review
        fields = ['id', 'content', 'game', 'gamer']
        depth = 1

class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'content', 'game']