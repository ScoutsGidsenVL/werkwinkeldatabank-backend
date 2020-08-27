from rest_framework import serializers
from datetime import timedelta
from drf_yasg.utils import swagger_serializer_method
from ...models import BuildingBlockTemplate, BuildingBlockInstance
from ...models.enums.building_block_type import BuildingBlockType
from .enum_serializers import EnumOutputSerializer
from ...helpers.enum_helper import parse_choice_to_tuple
from apps.serializer_extensions.serializers import DurationField
from pprint import pprint


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
class BuildingBlockInstanceCreateInputSerializer(BaseBuildingBlockCreateInputSerializer):
    template = serializers.PrimaryKeyRelatedField(queryset=BuildingBlockTemplate.objects.all())


class BuildingBlockInstanceUpdateInputSerializer(BaseBuildingBlockUpdateInputSerializer):
    template = serializers.PrimaryKeyRelatedField(queryset=BuildingBlockTemplate.objects.all(), required=False)
