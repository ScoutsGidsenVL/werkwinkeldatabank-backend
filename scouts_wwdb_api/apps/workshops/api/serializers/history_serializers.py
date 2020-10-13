from rest_framework import serializers
from ...models import History


# Output


class HistoryOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ("id", "data", "created_at")
