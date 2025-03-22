# pylint: disable=broad-exception-raised
"""apps.workshops.api.serializers.building_block_serializers."""

import datetime as dt

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from apps.base.serializers import DisabledFieldCreateInputSerializerMixin, DisabledFieldUpdateInputSerializerMixin
from apps.scouts_auth.api.serializers import UserNestedOutputSerializer
from apps.serializer_extensions.serializers import DurationField
from apps.workshops.api.serializers.category_serializers import CategoryDetailOutputSerializer
from apps.workshops.api.serializers.enum_serializers import EnumOutputSerializer
from apps.workshops.api.serializers.theme_serializers import ThemeDetailOutputSerializer
from apps.workshops.helpers.enum_helper import parse_choice_to_tuple
from apps.workshops.models import BuildingBlockInstance, BuildingBlockTemplate, Category, Theme
from apps.workshops.models.enums import BuildingBlockStatus, BuildingBlockType

# Output


class BuildingBlockTemplateDetailOutputSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    # Use own durationfield instead of existing one to get correct swagger documentation
    duration = DurationField()
    category = CategoryDetailOutputSerializer(read_only=True)
    created_by = UserNestedOutputSerializer(read_only=True)

    class Meta:
        model = BuildingBlockTemplate
        fields = (
            "id",
            "title",
            "description",
            "duration",
            "type",
            "category",
            "status",
            "short_description",
            "theme",
            "building_block_necessities",
            "created_by",
            "is_sensitive",
            "is_disabled",
            "created_at",
        )
        depth = 2

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_type(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(BuildingBlockType(obj.building_block_type))).data

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_status(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(BuildingBlockStatus(obj.status))).data

    def to_representation(self, instance):
        result = super().to_representation(instance)
        request = self.context.get("request")
        if not request:
            raise Exception("Make sure request has been given to the context of the serializer")
        if not request.user.has_perm("workshops.view_field_created_by_buildingblocktemplate"):
            result.pop("created_by")
        return result


class BuildingBlockTemplateListOutputSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    duration = DurationField()
    category = CategoryDetailOutputSerializer(read_only=True)
    theme = ThemeDetailOutputSerializer(read_only=True)

    class Meta:
        model = BuildingBlockTemplate
        fields = (
            "id",
            "title",
            "duration",
            "type",
            "short_description",
            "category",
            "status",
            "theme",
            "is_sensitive",
            "is_disabled",
            "last_edited",
            "created_by",
        )

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_type(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(BuildingBlockType(obj.building_block_type))).data

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_status(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(BuildingBlockStatus(obj.status))).data


class BuildingBlockInstanceNestedOutputSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    duration = DurationField()
    category = CategoryDetailOutputSerializer(read_only=True)
    theme = ThemeDetailOutputSerializer(read_only=True)
    template = serializers.PrimaryKeyRelatedField(read_only=True, pk_field=serializers.UUIDField())

    class Meta:
        model = BuildingBlockInstance
        fields = (
            "id",
            "title",
            "description",
            "duration",
            "type",
            "category",
            "theme",
            "order",
            "building_block_necessities",
            "is_sensitive",
            "linked_template_values",
            "template",
        )

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_type(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(BuildingBlockType(obj.building_block_type))).data


# Input


def get_theme_category_by_type_errors(type_, theme, category):
    errors = []
    if type_ == BuildingBlockType.THEMATIC:
        if not theme:
            errors.append(f"A building block of type {BuildingBlockType.THEMATIC.label} needs a theme")
        if category:
            errors.append(f"A building block of type {BuildingBlockType.THEMATIC.label} can't have a category")

    if type_ == BuildingBlockType.METHODIC:
        if not category:
            errors.append(f"A building block of type {BuildingBlockType.METHODIC.label} needs a category")
        if theme:
            errors.append(f"A building block of type {BuildingBlockType.METHODIC.label} can't have a theme")
    return errors


## Template
class BuildingBlockTemplateCreateInputSerializer(DisabledFieldCreateInputSerializerMixin, serializers.Serializer):
    type = serializers.ChoiceField(source="building_block_type", choices=BuildingBlockType.choices)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    duration = DurationField(min_value=dt.timedelta(minutes=0), max_value=dt.timedelta(days=1))
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False, allow_null=True)
    short_description = serializers.CharField(max_length=500, required=False, allow_blank=True)
    theme = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all(), required=False, allow_null=True)
    building_block_necessities = serializers.CharField(required=False, allow_blank=True)
    is_sensitive = serializers.BooleanField(required=False)

    def validate(self, attrs):
        errors = get_theme_category_by_type_errors(
            attrs.get("building_block_type"), attrs.get("theme"), attrs.get("category")
        )
        if errors:
            raise serializers.ValidationError(errors)
        return attrs


class BuildingBlockTemplateUpdateInputSerializer(DisabledFieldUpdateInputSerializerMixin, serializers.Serializer):
    type = serializers.ChoiceField(source="building_block_type", choices=BuildingBlockType.choices, required=False)
    title = serializers.CharField(max_length=200, required=False)
    description = serializers.CharField(required=False)
    duration = DurationField(min_value=dt.timedelta(minutes=0), max_value=dt.timedelta(days=1), required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False, allow_null=True)
    short_description = serializers.CharField(max_length=500, required=False, allow_blank=True)
    theme = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all(), required=False, allow_null=True)
    building_block_necessities = serializers.CharField(required=False, allow_blank=True)
    is_sensitive = serializers.BooleanField(required=False)

    def validate(self, attrs):
        errors = get_theme_category_by_type_errors(
            attrs.get("building_block_type", self.instance.building_block_type),
            attrs.get("theme", self.instance.theme),
            attrs.get("category", self.instance.category),
        )
        if errors:
            raise serializers.ValidationError(errors)
        return attrs


## Instance
class BuildingBlockInstanceNestedCreateInputSerializer(serializers.Serializer):
    template = serializers.PrimaryKeyRelatedField(queryset=BuildingBlockTemplate.objects.all())
    linked_template_values = serializers.BooleanField(default=False)
    title = serializers.CharField(max_length=200, required=False)
    description = serializers.CharField(required=False)
    duration = DurationField(min_value=dt.timedelta(minutes=0), max_value=dt.timedelta(days=1), required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False, allow_null=True)
    short_description = serializers.CharField(max_length=500, required=False)
    theme = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all(), required=False, allow_null=True)
    building_block_necessities = serializers.CharField(required=False)

    def validate(self, attrs):
        # If linked template values false then make certain fields required again
        if not attrs.get("linked_template_values", False):
            for field_name, _ in self.fields.items():
                required_fields = ["title", "description", "duration"]
                if field_name in required_fields and attrs.get(field_name, None) is None:
                    raise serializers.ValidationError({field_name: ["This field is required."]})
        template = attrs.get("template")
        errors = get_theme_category_by_type_errors(
            template.building_block_type,
            attrs.get("theme", template.theme if attrs.get("linked_template_values") else None),
            attrs.get("category", template.category if attrs.get("linked_template_values") else None),
        )
        if errors:
            raise serializers.ValidationError(errors)
        return attrs


class BuildingBlockInstanceNestedUpdateInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    linked_template_values = serializers.BooleanField(required=False)
    title = serializers.CharField(max_length=200, required=False)
    description = serializers.CharField(required=False)
    duration = DurationField(min_value=dt.timedelta(minutes=0), max_value=dt.timedelta(days=1), required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False, allow_null=True)
    short_description = serializers.CharField(max_length=500, required=False)
    theme = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all(), required=False, allow_null=True)
    building_block_necessities = serializers.CharField(required=False)

    def validate(self, attrs):
        # Calculate instance from root serializer
        self.instance = self.root.instance.building_blocks.get(pk=attrs.get("id"))

        if not self.instance:
            raise Exception("Cant update building block that isnt already related to workshop")
        # Set the linked_template_values boolean of instance to get correct properties for validation
        self.instance.linked_template_values = attrs.get("linked_template_values", self.instance.linked_template_values)

        errors = get_theme_category_by_type_errors(
            attrs.get("template", self.instance.template).building_block_type,
            attrs.get("theme", self.instance.theme),
            attrs.get("category", self.instance.category),
        )
        if errors:
            raise serializers.ValidationError(errors)
        return attrs
