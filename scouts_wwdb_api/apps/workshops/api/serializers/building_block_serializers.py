from rest_framework import serializers
from datetime import timedelta
from ...models import BuildingBlockTemplate, BuildingBlockInstance
from ...models.enums.building_block_type import BuildingBlockType
from .enum_serializers import EnumOutputSerializer
from ...helpers.enum_helper import parse_choice_to_tuple
from pprint import pprint


# Output


class BuildingBlockTemplateDetailOutputSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = BuildingBlockTemplate
        fields = ("id", "title", "description", "duration", "type")

    def get_type(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(BuildingBlockType(obj.building_block_type))).data


class BuildingBlockTemplateListOutputSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = BuildingBlockTemplate
        fields = ("id", "title", "description", "duration", "type")

    def get_type(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(BuildingBlockType(obj.building_block_type))).data


# Input


class BaseBuildingBlockCreateInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    duration = serializers.DurationField(min_value=timedelta(minutes=1), max_value=timedelta(days=1))


class BuildingBlockTemplateCreateInputSerializer(BaseBuildingBlockCreateInputSerializer):
    type = serializers.ChoiceField(source="building_block_type", choices=BuildingBlockType.choices)


class BaseBuildingBlockUpdateInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, required=False)
    description = serializers.CharField(required=False)
    duration = serializers.DurationField(min_value=timedelta(minutes=1), max_value=timedelta(days=1), required=False)


class BuildingBlockTemplateUpdateInputSerializer(BaseBuildingBlockUpdateInputSerializer):
    type = serializers.ChoiceField(source="building_block_type", choices=BuildingBlockType.choices, required=False)
