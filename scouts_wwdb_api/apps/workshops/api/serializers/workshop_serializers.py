from rest_framework import serializers
from datetime import timedelta
from drf_yasg.utils import swagger_serializer_method
from apps.serializer_extensions.serializers import DurationField, SerializerSwitchField
from ...models import Workshop, Theme
from ...models.enums.scouts_team import ScoutsTeam
from ...helpers.enum_helper import parse_choice_to_tuple
from .theme_serializers import ThemeDetailOutputSerializer
from .enum_serializers import EnumOutputSerializer
from apps.scouts_auth.api.serializers import UserNestedOutputSerializer
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
    created_by = UserNestedOutputSerializer(read_only=True)
    approving_team = serializers.SerializerMethodField()

    class Meta:
        model = Workshop
        fields = (
            "id",
            "title",
            "description",
            "short_description",
            "necessities",
            "workshop_status_type",
            "theme",
            "duration",
            "building_blocks",
            "created_by",
            "approving_team",
            "is_sensitive",
        )
        depth = 2

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_approving_team(self, obj):
        if obj.approving_team:
            return EnumOutputSerializer(parse_choice_to_tuple(ScoutsTeam(obj.approving_team))).data
        else:
            return None


class WorkshopListOutputSerializer(serializers.ModelSerializer):
    duration = DurationField()
    theme = ThemeDetailOutputSerializer(read_only=True)

    class Meta:
        model = Workshop
        fields = ("id", "title", "duration", "workshop_status_type", "theme", "short_description")


# Input


class WorkshopCreateInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    theme = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all())
    description = serializers.CharField()
    necessities = serializers.CharField(required=False)
    building_blocks = serializers.ListField(child=BuildingBlockInstanceNestedCreateInputSerializer(), min_length=1)
    short_description = serializers.CharField(max_length=500, required=False)
    approving_team = serializers.ChoiceField(choices=ScoutsTeam.choices, required=False)


class WorkshopUpdateInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, required=False)
    theme = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all(), required=False)
    description = serializers.CharField(required=False)
    necessities = serializers.CharField(required=False)
    building_blocks = serializers.ListField(
        child=SerializerSwitchField(
            create_serializer=BuildingBlockInstanceNestedCreateInputSerializer(),
            update_serializer=BuildingBlockInstanceNestedUpdateInputSerializer(),
        ),
        min_length=1,
        required=False,
    )
    short_description = serializers.CharField(max_length=500, required=False)
    approving_team = serializers.ChoiceField(choices=ScoutsTeam.choices, required=False)

    def validate_building_blocks(self, value):
        # Check whether if an id was given for building block it is already linked to current workshop
        current_workshop = self.instance
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
