from rest_framework import serializers
from datetime import timedelta
from drf_yasg.utils import swagger_serializer_method
from ...models import BuildingBlockTemplate, BuildingBlockInstance
from ...models.enums.building_block_type import BuildingBlockType
from .enum_serializers import EnumOutputSerializer
from ...helpers.enum_helper import parse_choice_to_tuple
from apps.serializer_extensions.serializers import DurationField


# Output


class BuildingBlockTemplateDetailOutputSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    # Use own durationfield instead of existing one to get correct swagger documentation
    duration = DurationField()

    class Meta:
        model = BuildingBlockTemplate
        fields = ("id", "title", "description", "duration", "type")

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_type(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(BuildingBlockType(obj.building_block_type))).data


class BuildingBlockTemplateListOutputSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    duration = DurationField()

    class Meta:
        model = BuildingBlockTemplate
        fields = ("id", "title", "description", "duration", "type")

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_type(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(BuildingBlockType(obj.building_block_type))).data


class BuildingBlockInstanceNestedOutputSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    duration = DurationField()

    class Meta:
        model = BuildingBlockInstance
        fields = ("id", "title", "description", "duration", "type")

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_type(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(BuildingBlockType(obj.building_block_type))).data


# Input

## Base
class BaseBuildingBlockCreateInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    duration = DurationField(min_value=timedelta(minutes=1), max_value=timedelta(days=1))


class BaseBuildingBlockUpdateInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, required=False)
    description = serializers.CharField(required=False)
    duration = DurationField(min_value=timedelta(minutes=1), max_value=timedelta(days=1), required=False)


## Template
class BuildingBlockTemplateCreateInputSerializer(BaseBuildingBlockCreateInputSerializer):
    type = serializers.ChoiceField(source="building_block_type", choices=BuildingBlockType.choices)


class BuildingBlockTemplateUpdateInputSerializer(BaseBuildingBlockUpdateInputSerializer):
    type = serializers.ChoiceField(source="building_block_type", choices=BuildingBlockType.choices, required=False)


## Instance
class BuildingBlockInstanceNestedCreateInputSerializer(BaseBuildingBlockCreateInputSerializer):
    template = serializers.PrimaryKeyRelatedField(queryset=BuildingBlockTemplate.objects.all())


class BuildingBlockInstanceNestedUpdateInputSerializer(BaseBuildingBlockUpdateInputSerializer):
    id = serializers.UUIDField(required=False)
    template = serializers.PrimaryKeyRelatedField(queryset=BuildingBlockTemplate.objects.all(), required=False)

    def to_internal_value(self, data):
        # If id given then template should get ignored because we shouldnt change template of existing building block
        if data.get("id", None):
            try:
                data.pop("template")
            except KeyError:
                pass
        return super().to_internal_value(data)

    def validate(self, data):
        # If no id given then do required check for all fields that are not id
        if not data.get("id", None):
            for field_name, field in self.fields.items():
                if field_name != "id" and not data.get(field_name, None):
                    raise serializers.ValidationError({field_name: ["This field is required."]})
        return data
