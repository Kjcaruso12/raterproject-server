from django.db import models

class Rating(models.Model):
    value = models.IntegerField(default=None)
    game = models.ForeignKey("game", on_delete=models.CASCADE)
    gamer = models.ForeignKey("gamer", on_delete=models.CASCADE)