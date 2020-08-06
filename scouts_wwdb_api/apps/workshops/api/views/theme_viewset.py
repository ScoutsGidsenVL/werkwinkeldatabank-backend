from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from ..serializers.theme_serializers import (
    ThemeCreateInputSerializer,
    ThemeDetailOutputSerializer,
    ThemeListOutputSerializer,
    ThemeUpdateInputSerializer,
)
from ...services.theme_service import theme_create, theme_update
from ...models import Theme


class ThemeViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={status.HTTP_200_OK: ThemeDetailOutputSerializer})
    def retrieve(self, request, pk=None):
        theme = get_object_or_404(Theme.objects, pk=pk)
        serializer = ThemeDetailOutputSerializer(theme)

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ThemeCreateInputSerializer, responses={status.HTTP_201_CREATED: ThemeDetailOutputSerializer}
    )
    def create(self, request):
        input_serializer = ThemeCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        created_theme = theme_create(**input_serializer.validated_data)

        output_serializer = ThemeDetailOutputSerializer(created_theme)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: ThemeListOutputSerializer})
    def list(self, request):
        themes = Theme.objects.all()
        serializer = ThemeListOutputSerializer(themes, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ThemeUpdateInputSerializer, responses={status.HTTP_200_OK: ThemeDetailOutputSerializer}
    )
    def partial_update(self, request, pk=None):
        theme = get_object_or_404(Theme.objects, pk=pk)

        serializer = ThemeUpdateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_theme = theme_update(existing_theme=theme, **serializer.validated_data)
        updated_theme.save()

        output_serializer = ThemeDetailOutputSerializer(updated_theme)

        return Response(output_serializer.data)
