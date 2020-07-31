from rest_framework import serializers
from ...models import Workshop


# Output


class WorkshopDetailOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = "__all__"


class WorkshopListOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = ("id", "title")


# Input


class WorkshopCreateInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    duration = serializers.CharField(max_length=50)
    theme = serializers.UUIDField()
    description = serializers.CharField()
    necessities = serializers.CharField()


class WorkshopUpdateInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    duration = serializers.CharField(max_length=50)
    description = serializers.CharField()
    necessities = serializers.CharField()

