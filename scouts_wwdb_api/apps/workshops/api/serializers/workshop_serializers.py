from rest_framework import serializers
from datetime import timedelta
from apps.serializer_extensions.serializers import DurationField
from ...models import Workshop, Theme
from .theme_serializers import ThemeDetailOutputSerializer
from .building_block_serializers import (
    BuildingBlockInstanceNestedCreateInputSerializer,
    BuildingBlockInstanceNestedUpdateInputSerializer,
    BuildingBlockInstanceNestedOutputSerializer,
)
from pprint import pprint

# Output


class WorkshopDetailOutputSerializer(serializers.ModelSerializer):
    theme = ThemeDetailOutputSerializer(read_only=True)
    duration = DurationField()
    building_blocks = BuildingBlockInstanceNestedOutputSerializer(many=True, read_only=True)

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
    building_blocks = serializers.ListField(child=BuildingBlockInstanceNestedCreateInputSerializer(), min_length=1)


class WorkshopUpdateInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, required=False)
    duration = DurationField(min_value=timedelta(minutes=1), max_value=timedelta(days=7), required=False)
    theme = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all(), required=False)
    description = serializers.CharField(required=False)
    necessities = serializers.CharField(required=False)
    building_blocks = serializers.ListField(
        child=BuildingBlockInstanceNestedUpdateInputSerializer(), min_length=1, required=False
    )

    def validate_building_blocks(self, value):
        # Check whether if an id was given for building block it is already linked to current workshop
        current_workshop = self.context.get("instance", None)
        if not current_workshop:
            raise Exception("Context for workshop update input serializer should contain an instance")

        current_block_ids = current_workshop.building_blocks.values_list("id", flat=True)
        for building_block in value:
            block_id = building_block.get("id", None)
            if block_id and block_id not in current_block_ids:
                raise serializers.ValidationError(
                    'Invalid id given "{}", only building blocks that have already been added to the workshop can be updated'.format(
                        block_id
                    )
                )

        return value
