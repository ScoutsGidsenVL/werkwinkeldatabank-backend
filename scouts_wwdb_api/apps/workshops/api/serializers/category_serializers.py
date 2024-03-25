"""apps.workshops.api.serializers.category_serializers."""
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.base.serializers import DisabledFieldCreateInputSerializerMixin, DisabledFieldUpdateInputSerializerMixin

from ...models import Category


class CategoryDetailOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "title", "is_disabled")


class CategoryListOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "title", "is_disabled")


class CategoryCreateInputSerializer(DisabledFieldCreateInputSerializerMixin, serializers.Serializer):
    title = serializers.CharField(max_length=200, validators=[UniqueValidator(queryset=Category.objects.all())])


class CategoryUpdateInputSerializer(DisabledFieldUpdateInputSerializerMixin, serializers.Serializer):
    title = serializers.CharField(
        max_length=200, validators=[UniqueValidator(queryset=Category.objects.all())], required=False
    )
