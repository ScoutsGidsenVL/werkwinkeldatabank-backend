from rest_framework import serializers
from datetime import timedelta
from drf_yasg2.utils import swagger_serializer_method
from apps.serializer_extensions.serializers import DurationField, SerializerSwitchField, PermissionRequiredField
from apps.base.serializers import DisabledFieldCreateInputSerializerMixin, DisabledFieldUpdateInputSerializerMixin
from apps.files.models import CKEditorFile
from ...models import Workshop, Theme
from ...models.enums.scouts_team import ScoutsTeam
from ...helpers.enum_helper import parse_choice_to_tuple
from .theme_serializers import ThemeDetailOutputSerializer
from apps.files.api.serializers import FileDetailOutputSerializer
from .enum_serializers import EnumOutputSerializer
from apps.scouts_auth.api.serializers import UserNestedOutputSerializer
from .building_block_serializers import (
    BuildingBlockInstanceNestedCreateInputSerializer,
    BuildingBlockInstanceNestedUpdateInputSerializer,
    BuildingBlockInstanceNestedOutputSerializer,
)

# Output


class WorkshopDetailOutputSerializer(serializers.ModelSerializer):
    themes = ThemeDetailOutputSerializer(read_only=True, many=True)
    files = FileDetailOutputSerializer(read_only=True, many=True)
    duration = DurationField()
    building_blocks = BuildingBlockInstanceNestedOutputSerializer(many=True, read_only=True)
    created_by = UserNestedOutputSerializer(read_only=True)
    approving_team = serializers.SerializerMethodField()
    is_mine = serializers.SerializerMethodField()

    class Meta:
        model = Workshop
        fields = (
            "id",
            "title",
            "description",
            "short_description",
            "necessities",
            "workshop_status_type",
            "themes",
            "files",
            "duration",
            "building_blocks",
            "created_by",
            "approving_team",
            "is_mine",
            "is_sensitive",
            "is_disabled",
            "created_at",
            "published_at",
        )
        depth = 2

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_approving_team(self, obj):
        if obj.approving_team:
            return EnumOutputSerializer(parse_choice_to_tuple(ScoutsTeam(obj.approving_team))).data
        else:
            return None

    def get_is_mine(self, obj):
        request = self.context.get("request")
        if not request:
            raise Exception("Make sure request has been given to the context of the serializer")
        return request.user == obj.created_by

    def to_representation(self, value):
        result = super().to_representation(value)
        request = self.context.get("request")
        if not request:
            raise Exception("Make sure request has been given to the context of the serializer")
        if not request.user.has_perm("workshops.view_field_created_by_workshop"):
            result.pop("created_by")
        if not request.user.has_perm("workshops.view_field_is_sensitive_workshop"):
            result.pop("is_sensitive")
        return result


class WorkshopListOutputSerializer(serializers.ModelSerializer):
    duration = DurationField()
    themes = ThemeDetailOutputSerializer(read_only=True, many=True)

    class Meta:
        model = Workshop
        fields = (
            "id",
            "title",
            "duration",
            "workshop_status_type",
            "themes",
            "short_description",
            "is_sensitive",
            "is_disabled",
            "created_at",
            "published_at",
        )


# Input


class WorkshopCreateInputSerializer(DisabledFieldCreateInputSerializerMixin, serializers.Serializer):
    title = serializers.CharField(max_length=200)
    themes = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all(), many=True)
    files = serializers.PrimaryKeyRelatedField(queryset=CKEditorFile.objects.all(), many=True)
    description = serializers.CharField()
    necessities = serializers.CharField(required=False, allow_blank=True)
    building_blocks = serializers.ListField(child=BuildingBlockInstanceNestedCreateInputSerializer(), min_length=1)
    short_description = serializers.CharField(max_length=500, required=False, allow_blank=True)
    approving_team = serializers.ChoiceField(
        choices=ScoutsTeam.choices, required=False, allow_null=True, allow_blank=True
    )

    def validate_themes(self, attrs):
        if len(attrs) < 1:
            raise serializers.ValidationError("At least one theme required")
        return attrs


class WorkshopUpdateInputSerializer(DisabledFieldUpdateInputSerializerMixin, serializers.Serializer):
    title = serializers.CharField(max_length=200, required=False)
    themes = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all(), required=False, many=True)
    files = serializers.PrimaryKeyRelatedField(queryset=CKEditorFile.objects.all(), required=False, many=True)
    description = serializers.CharField(required=False)
    necessities = serializers.CharField(required=False, allow_blank=True)
    building_blocks = serializers.ListField(
        child=SerializerSwitchField(
            create_serializer=BuildingBlockInstanceNestedCreateInputSerializer(),
            update_serializer=BuildingBlockInstanceNestedUpdateInputSerializer(),
        ),
        min_length=1,
        required=False,
    )
    short_description = serializers.CharField(max_length=500, required=False, allow_blank=True)
    approving_team = serializers.ChoiceField(
        choices=ScoutsTeam.choices, required=False, allow_null=True, allow_blank=True
    )

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
