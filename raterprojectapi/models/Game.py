from django.db import models
from raterprojectapi.models.Category import Category
from raterprojectapi.models.Rating import Rating


class Game(models.Model):
    title = models.CharField(max_length=55)
    description = models.CharField(max_length=100)
    designer = models.CharField(max_length=55)
    year_released = models.IntegerField(default=None)
    number_of_players = models.IntegerField(default=None)
    estimated_time_to_play = models.IntegerField(default=None)
    age_recommendation = models.IntegerField()
    gamer = models.ForeignKey("gamer", on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name="categories")

    @property
    def average_rating(self):
        """Average rating calculated attribute for each game"""
        ratings = Rating.objects.filter(game=self)

        # Sum all of the ratings for the game
        total_rating = 0
        for rating in ratings:
            total_rating += rating.value
        total_rating = total_rating / len(ratings)
        return total_rating
        # Calculate the average and return it.
        # If you don't know how to calculate average, Google it.