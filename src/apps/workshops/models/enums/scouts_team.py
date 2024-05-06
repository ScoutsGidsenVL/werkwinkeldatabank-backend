"""apps.workshops.models.enums.scouts_team."""
from django.db import models


class ScoutsTeam(models.TextChoices):
    GROUP1 = "GROUP1", "Vorming"
    GROUP2 = "GROUP2", "Diversiteit"
    GROUP3 = "GROUP3", "Ecologie"
    GROUP4 = "GROUP4", "Internationaal"
    GROUP5 = "GROUP5", "IT"
    GROUP6 = "GROUP6", "Lokalen"
    GROUP7 = "GROUP7", "Technieken"
    GROUP8 = "GROUP8", "Zingeving"
    GROUP9 = "GROUP9", "Kapoenen"
    GROUP10 = "GROUP10", "Kabouters & Welpen"
    GROUP11 = "GROUP11", "Jonggivers"
    GROUP12 = "GROUP12", "Givers"
    GROUP13 = "GROUP13", "Jins"
    GROUP14 = "GROUP14", "Groepsleiding"
    GROUP15 = "GROUP15", "Akabe"
    GROUP16 = "GROUP16", "Zeescouting"
