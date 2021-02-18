from rest_framework import serializers
from apps.base.serializers import DisabledFieldCreateInputSerializerMixin, DisabledFieldUpdateInputSerializerMixin
from ...models import Theme


# Output


class ThemeDetailOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ("id", "title", "description", "is_disabled")


class ThemeListOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ("id", "title", "is_disabled")


# Input


class ThemeCreateInputSerializer(DisabledFieldCreateInputSerializerMixin, serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False)


class ThemeUpdateInputSerializer(DisabledFieldUpdateInputSerializerMixin, serializers.Serializer):
    title = serializers.CharField(max_length=200, required=False)
    description = serializers.CharField(required=False)
