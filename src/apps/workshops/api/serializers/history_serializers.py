"""apps.workshops.api.serializers.history_serializers."""
from rest_framework import serializers

from ...models import History


class HistoryOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ("id", "data", "created_at")
