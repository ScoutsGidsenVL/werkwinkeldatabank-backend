from rest_framework import serializers
from datetime import timedelta
from apps.serializer_extensions.serializers import DurationField
from ...models import Workshop, Theme
from .theme_serializers import ThemeDetailOutputSerializer


# Output


class WorkshopDetailOutputSerializer(serializers.ModelSerializer):
    theme = ThemeDetailOutputSerializer(read_only=True)
    duration = DurationField()

    class Meta:
        model = Workshop
        fields = "__all__"
        depth = 2


class WorkshopListOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = ("id", "title")


# Input


class WorkshopCreateInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    duration = DurationField(min_value=timedelta(minutes=1), max_value=timedelta(days=7))
    theme = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all())
    description = serializers.CharField()
    necessities = serializers.CharField()


class WorkshopUpdateInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, required=False)
    duration = DurationField(min_value=timedelta(minutes=1), max_value=timedelta(days=7), required=False)
    theme = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all(), required=False)
    description = serializers.CharField(required=False)
    necessities = serializers.CharField(required=False)
