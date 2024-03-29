"""apps.workshops.serializers.building_block_serializers."""
import datetime as dt

from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from apps.base.serializers import DisabledFieldCreateInputSerializerMixin, DisabledFieldUpdateInputSerializerMixin
from apps.scouts_auth.api.serializers import UserNestedOutputSerializer
from apps.serializer_extensions.serializers import DurationField

from ...helpers.enum_helper import parse_choice_to_tuple
from ...models import BuildingBlockInstance, BuildingBlockTemplate, Category, Theme
from ...models.enums import BuildingBlockStatus, BuildingBlockType
from .category_serializers import CategoryDetailOutputSerializer
from .enum_serializers import EnumOutputSerializer
from .theme_serializers import ThemeDetailOutputSerializer

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

    def to_representation(self, value):
        result = super().to_representation(value)
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


def get_theme_category_by_type_errors(type, theme, category):
    errors = []
    if type == BuildingBlockType.THEMATIC:
        if not theme:
            errors.append("A building block of type %s needs a theme" % BuildingBlockType.THEMATIC.label)
        if category:
            errors.append("A building block of type %s can't have a category" % BuildingBlockType.THEMATIC.label)

    if type == BuildingBlockType.METHODIC:
        if not category:
            errors.append("A building block of type %s needs a category" % BuildingBlockType.METHODIC.label)
        if theme:
            errors.append("A building block of type %s can't have a theme" % BuildingBlockType.METHODIC.label)
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

    def validate(self, data):
        errors = get_theme_category_by_type_errors(
            data.get("building_block_type"), data.get("theme"), data.get("category")
        )
        if errors:
            raise serializers.ValidationError(errors)
        return data


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

    def validate(self, data):
        errors = get_theme_category_by_type_errors(
            data.get("building_block_type", self.instance.building_block_type),
            data.get("theme", self.instance.theme),
            data.get("category", self.instance.category),
        )
        if errors:
            raise serializers.ValidationError(errors)
        return data


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

    def validate(self, data):
        # If linked template values false then make certain fields required again
        if not data.get("linked_template_values", False):
            for field_name, field in self.fields.items():
                required_fields = ["title", "description", "duration"]
                if field_name in required_fields and data.get(field_name, None) is None:
                    raise serializers.ValidationError({field_name: ["This field is required."]})
        template = data.get("template")
        errors = get_theme_category_by_type_errors(
            template.building_block_type,
            data.get("theme", template.theme if data.get("linked_template_values") else None),
            data.get("category", template.category if data.get("linked_template_values") else None),
        )
        if errors:
            raise serializers.ValidationError(errors)
        return data


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

    def validate(self, data):
        # Calculate instance from root serializer
        self.instance = self.root.instance.building_blocks.get(pk=data.get("id"))

        if not self.instance:
            raise Exception("Cant update building block that isnt already related to workshop")
        # Set the linked_template_values boolean of instance to get correct properties for validation
        self.instance.linked_template_values = data.get("linked_template_values", self.instance.linked_template_values)

        errors = get_theme_category_by_type_errors(
            data.get("template", self.instance.template).building_block_type,
            data.get("theme", self.instance.theme),
            data.get("category", self.instance.category),
        )
        if errors:
            raise serializers.ValidationError(errors)
        return data
