from rest_framework import serializers
from ...models import Workshop


# Output


class WorkshopDetailOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = ("id", "title", "duration", "theme", "description", "necessities")


# Input



