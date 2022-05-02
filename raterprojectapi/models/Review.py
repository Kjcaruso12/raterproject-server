from django.db import models

class Review(models.Model):
    content = models.CharField(max_length=200)
    game = models.ForeignKey("game", on_delete=models.CASCADE)
    gamer = models.ForeignKey("gamer", on_delete=models.CASCADE)