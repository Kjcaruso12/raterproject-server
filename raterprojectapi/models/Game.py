from django.db import models
from raterprojectapi.models.Category import Category


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