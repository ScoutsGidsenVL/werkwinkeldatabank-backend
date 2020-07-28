from django.db import models
from .theme import Theme

class Workshop(models.Model):
    title = models.CharField(max_length=200)
    duration = models.CharField(max_length=50)
    theme = models.ManyToManyField(Theme)
    description = models.TextField()
    necessities = models.TextField()

    def __str__(self):
        return self.title