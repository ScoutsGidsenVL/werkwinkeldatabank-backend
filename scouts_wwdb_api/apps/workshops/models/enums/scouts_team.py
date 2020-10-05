from django.db import models


class ScoutsTeam(models.TextChoices):
    GROUP1 = "GROUP1", "Ploeg 1"
    GROUP2 = "GROUP2", "Ploeg 2"
