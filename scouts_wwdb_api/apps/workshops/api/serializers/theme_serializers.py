from rest_framework import serializers
from ...models import Theme


# Output


class ThemeDetailOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ("id", "title", "description")


class ThemeListOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Theme
        fields = ("id", "title")


# Input


class ThemeCreateInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()

class ThemeUpdateInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
