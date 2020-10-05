from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from ..serializers.building_block_serializers import (
    BuildingBlockTemplateCreateInputSerializer,
    BuildingBlockTemplateDetailOutputSerializer,
    BuildingBlockTemplateListOutputSerializer,
    BuildingBlockTemplateUpdateInputSerializer,
)
from ...services.building_block_template_service import building_block_template_create, building_block_template_update
from ...models import BuildingBlockTemplate
from ..filters.building_block_template_filter import BuildingBlockTemplateFilter


class BuildingBlockTemplateViewSet(viewsets.GenericViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = BuildingBlockTemplateFilter

    def get_queryset(self):
        return BuildingBlockTemplate.objects.all()

    @swagger_auto_schema(responses={status.HTTP_200_OK: BuildingBlockTemplateDetailOutputSerializer})
    def retrieve(self, request, pk=None):
        template = get_object_or_404(BuildingBlockTemplate.objects, pk=pk)
        serializer = BuildingBlockTemplateDetailOutputSerializer(template)

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=BuildingBlockTemplateCreateInputSerializer,
        responses={status.HTTP_201_CREATED: BuildingBlockTemplateDetailOutputSerializer},
    )
    def create(self, request):
        input_serializer = BuildingBlockTemplateCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        created_template = building_block_template_create(**input_serializer.validated_data)

        output_serializer = BuildingBlockTemplateDetailOutputSerializer(created_template)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: BuildingBlockTemplateListOutputSerializer})
    def list(self, request):
        results = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(results)

        if page is not None:
            serializer = BuildingBlockTemplateListOutputSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = BuildingBlockTemplateListOutputSerializer(results, many=True)
            return Response(serializer.data)

    @swagger_auto_schema(
        request_body=BuildingBlockTemplateUpdateInputSerializer,
        responses={status.HTTP_200_OK: BuildingBlockTemplateDetailOutputSerializer},
    )
    def partial_update(self, request, pk=None):
        template = get_object_or_404(BuildingBlockTemplate.objects, pk=pk)

        serializer = BuildingBlockTemplateUpdateInputSerializer(data=request.data, instance=template)
        serializer.is_valid(raise_exception=True)

        updated_template = building_block_template_update(existing_template=template, **serializer.validated_data)

        output_serializer = BuildingBlockTemplateDetailOutputSerializer(updated_template)

        return Response(output_serializer.data)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: BuildingBlockTemplateDetailOutputSerializer},
    )
    @action(detail=False, methods=["get"], url_path="empty_default")
    def get_empty_default(self, request):
        template = BuildingBlockTemplate.objects.get_empty_default()
        output_serializer = BuildingBlockTemplateDetailOutputSerializer(template)

        return Response(output_serializer.data)
