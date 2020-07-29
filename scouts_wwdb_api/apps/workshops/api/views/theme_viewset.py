from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..serializers.theme_serializers import ThemeCreateInputSerializer, ThemeDetailOutputSerializer
from ...services.theme_service import theme_create
from ...models import Theme


class ThemeViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        # theme = get_object_or_404(Theme.objects, pk=pk)
        theme = Theme.objects.get(pk=pk)

        serializer = ThemeDetailOutputSerializer(theme)

        return Response(serializer.data)

    def create(self, request):
        input_serializer = ThemeCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        created_theme = theme_create(**input_serializer.validated_data)

        output_serializer = ThemeDetailOutputSerializer(created_theme)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
