from rest_framework import serializers
from datetime import timedelta
from drf_yasg.utils import swagger_serializer_method
from apps.base.serializers import DisabledFieldCreateInputSerializerMixin, DisabledFieldUpdateInputSerializerMixin
from ...models import BuildingBlockTemplate, BuildingBlockInstance, Category, Theme
from ...models.enums.building_block_type import BuildingBlockType
from .enum_serializers import EnumOutputSerializer
from .category_serializers import CategoryDetailOutputSerializer
from ...helpers.enum_helper import parse_choice_to_tuple
from apps.serializer_extensions.serializers import DurationField
from .theme_serializers import ThemeDetailOutputSerializer

# Output


class BuildingBlockTemplateDetailOutputSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    # Use own durationfield instead of existing one to get correct swagger documentation
    duration = DurationField()
    category = CategoryDetailOutputSerializer(read_only=True)

    class Meta:
        model = BuildingBlockTemplate
        fields = (
            "id",
            "title",
            "description",
            "duration",
            "type",
            "category",
            "short_description",
            "theme",
            "building_block_necessities",
            "is_sensitive",
            "is_disabled",
        )
        depth = 2

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_type(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(BuildingBlockType(obj.building_block_type))).data


class BuildingBlockTemplateListOutputSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
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
            "theme",
            "is_sensitive",
            "is_disabled",
        )

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_type(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(BuildingBlockType(obj.building_block_type))).data


class BuildingBlockInstanceNestedOutputSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    duration = DurationField()

    class Meta:
        model = BuildingBlockInstance
        fields = (
            "id",
            "title",
            "description",
            "duration",
            "type",
            "order",
            "building_block_necessities",
            "is_sensitive",
            "linked_template_values",
        )

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_type(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(BuildingBlockType(obj.building_block_type))).data


# Input

## Template
class BuildingBlockTemplateCreateInputSerializer(DisabledFieldCreateInputSerializerMixin, serializers.Serializer):
    type = serializers.ChoiceField(source="building_block_type", choices=BuildingBlockType.choices)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    duration = DurationField(min_value=timedelta(minutes=1), max_value=timedelta(days=1))
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)
    short_description = serializers.CharField(max_length=500, required=False)
    theme = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all(), required=False)
    building_block_necessities = serializers.CharField(required=False)
    is_sensitive = serializers.BooleanField(required=False)


class BuildingBlockTemplateUpdateInputSerializer(DisabledFieldUpdateInputSerializerMixin, serializers.Serializer):
    type = serializers.ChoiceField(source="building_block_type", choices=BuildingBlockType.choices, required=False)
    title = serializers.CharField(max_length=200, required=False)
    description = serializers.CharField(required=False)
    duration = DurationField(min_value=timedelta(minutes=1), max_value=timedelta(days=1), required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)
    short_description = serializers.CharField(max_length=500, required=False)
    theme = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all(), required=False)
    building_block_necessities = serializers.CharField(required=False)
    is_sensitive = serializers.BooleanField(required=False)


## Instance
class BuildingBlockInstanceNestedCreateInputSerializer(serializers.Serializer):
    template = serializers.PrimaryKeyRelatedField(queryset=BuildingBlockTemplate.objects.all())
    linked_template_values = serializers.BooleanField(default=False)
    title = serializers.CharField(max_length=200, required=False)
    description = serializers.CharField(required=False)
    duration = DurationField(min_value=timedelta(minutes=1), max_value=timedelta(days=1), required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)
    short_description = serializers.CharField(max_length=500, required=False)
    theme = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all(), required=False)
    building_block_necessities = serializers.CharField(required=False)

    def validate(self, data):
        # If linked template values false then make certain fields required again
        if not data.get("linked_template_values", False):
            for field_name, field in self.fields.items():
                required_fields = ["title", "description", "duration"]
                if field_name in required_fields and not data.get(field_name, None):
                    raise serializers.ValidationError({field_name: ["This field is required."]})
        return data


class BuildingBlockInstanceNestedUpdateInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    linked_template_values = serializers.BooleanField(required=False)
    title = serializers.CharField(max_length=200, required=False)
    description = serializers.CharField(required=False)
    duration = DurationField(min_value=timedelta(minutes=1), max_value=timedelta(days=1), required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)
    short_description = serializers.CharField(max_length=500, required=False)
    theme = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all(), required=False)
    building_block_necessities = serializers.CharField(required=False)
