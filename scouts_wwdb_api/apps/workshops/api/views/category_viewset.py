from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_yasg2.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from apps.scouts_auth.permissions import ExtendedDjangoModelPermissions, CustomDjangoPermission
from ..serializers.category_serializers import (
    CategoryCreateInputSerializer,
    CategoryDetailOutputSerializer,
    CategoryListOutputSerializer,
    CategoryUpdateInputSerializer,
)
from ...services.category_service import category_create, category_update
from ...models import Category
from ..filters.category_filter import CategoryFilter


class CategoryViewSet(viewsets.GenericViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter
    permission_classes = [ExtendedDjangoModelPermissions]

    def get_queryset(self):
        return Category.objects.all().allowed(self.request.user)

    def get_permissions(self):
        current_permissions = super().get_permissions()
        if self.action in ("retrieve", "list"):
            return [permissions.AllowAny()]

        return current_permissions

    @swagger_auto_schema(responses={status.HTTP_200_OK: CategoryDetailOutputSerializer})
    def retrieve(self, request, pk=None):
        category = self.get_object()
        serializer = CategoryDetailOutputSerializer(category)

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CategoryCreateInputSerializer, responses={status.HTTP_201_CREATED: CategoryDetailOutputSerializer}
    )
    def create(self, request):
        input_serializer = CategoryCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        created_category = category_create(**input_serializer.validated_data)

        output_serializer = CategoryDetailOutputSerializer(created_category)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CategoryListOutputSerializer})
    def list(self, request):
        categories = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(categories)

        if page is not None:
            serializer = CategoryListOutputSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = CategoryListOutputSerializer(categories, many=True)
            return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CategoryUpdateInputSerializer, responses={status.HTTP_200_OK: CategoryDetailOutputSerializer}
    )
    def partial_update(self, request, pk=None):
        category = self.get_object()

        serializer = CategoryUpdateInputSerializer(data=request.data, instance=category, context={"request": request})

        serializer.is_valid(raise_exception=True)

        updated_category = category_update(existing_category=category, **serializer.validated_data)

        output_serializer = CategoryDetailOutputSerializer(updated_category)

        return Response(output_serializer.data)
