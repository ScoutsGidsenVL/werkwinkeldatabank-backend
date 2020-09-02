from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from ...models import Category


# Output


class CategoryDetailOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "title")


class CategoryListOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "title")


# Input


class CategoryCreateInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, validators=[UniqueValidator(queryset=Category.objects.all())])


class CategoryUpdateInputSerializer(serializers.Serializer):
    title = serializers.CharField(
        max_length=200, validators=[UniqueValidator(queryset=Category.objects.all())], required=False
    )
