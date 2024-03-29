from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.scouts_auth.permissions import CustomDjangoPermission, ExtendedDjangoModelPermissions

from ...exceptions import InvalidWorkflowTransitionException
from ...models import BuildingBlockTemplate
from ...services.building_block_template_service import (
    building_block_template_add_history,
    building_block_template_create,
    building_block_template_publish,
    building_block_template_request_publication,
    building_block_template_unpublish,
    building_block_template_update,
)
from ..exceptions import InvalidWorkflowTransitionAPIException
from ..filters.building_block_template_filter import BuildingBlockTemplateFilter
from ..permissions import BuildingBlockTemplateChangePermission
from ..serializers.building_block_serializers import (
    BuildingBlockTemplateCreateInputSerializer,
    BuildingBlockTemplateDetailOutputSerializer,
    BuildingBlockTemplateListOutputSerializer,
    BuildingBlockTemplateUpdateInputSerializer,
)
from ..serializers.history_serializers import HistoryOutputSerializer


class BuildingBlockTemplateViewSet(viewsets.GenericViewSet):
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = BuildingBlockTemplateFilter
    permission_classes = [ExtendedDjangoModelPermissions]
    ordering_fields = ["updated_at", "created_at"]
    ordering = ["-updated_at"]

    def get_queryset(self):
        return BuildingBlockTemplate.objects.all().order_by("last_edited").non_empty().allowed(self.request.user)

    def get_permissions(self):
        current_permissions = super().get_permissions()
        if self.action in ("retrieve", "list", "get_empty_default"):
            return [permissions.AllowAny()]
        if self.action == "history":
            current_permissions.append(CustomDjangoPermission("workshops.view_history"))
        if self.action == "partial_update":
            current_permissions.append(BuildingBlockTemplateChangePermission())
        if self.action == "request_publication":
            current_permissions.extend(
                [
                    CustomDjangoPermission("workshops.request_publication_buildingblocktemplate"),
                    BuildingBlockTemplateChangePermission(),
                ]
            )
        if self.action == "publish":
            current_permissions.append(CustomDjangoPermission("workshops.publish_buildingblocktemplate"))
        if self.action == "unpublish":
            current_permissions.append(CustomDjangoPermission("workshops.unpublish_buildingblocktemplate"))

        return current_permissions

    def handle_exception(self, exc):
        if isinstance(exc, InvalidWorkflowTransitionException):
            exc = InvalidWorkflowTransitionAPIException(exc)

        return super().handle_exception(exc)

    @swagger_auto_schema(responses={status.HTTP_200_OK: BuildingBlockTemplateDetailOutputSerializer})
    def retrieve(self, request, pk=None):
        template = self.get_object()
        serializer = BuildingBlockTemplateDetailOutputSerializer(template, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=BuildingBlockTemplateCreateInputSerializer,
        responses={status.HTTP_201_CREATED: BuildingBlockTemplateDetailOutputSerializer},
    )
    def create(self, request):
        input_serializer = BuildingBlockTemplateCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        created_template = building_block_template_create(**input_serializer.validated_data, created_by=request.user)

        output_serializer = BuildingBlockTemplateDetailOutputSerializer(created_template, context={"request": request})

        # Save data json in history to get easy history
        building_block_template_add_history(data=output_serializer.data, template=created_template)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: BuildingBlockTemplateListOutputSerializer})
    def list(self, request):
        results = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(results)

        if page is not None:
            serializer = BuildingBlockTemplateListOutputSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        else:
            serializer = BuildingBlockTemplateListOutputSerializer(results, many=True, context={"request": request})
            return Response(serializer.data)

    @swagger_auto_schema(
        request_body=BuildingBlockTemplateUpdateInputSerializer,
        responses={status.HTTP_200_OK: BuildingBlockTemplateDetailOutputSerializer},
    )
    def partial_update(self, request, pk=None):
        template = self.get_object()

        serializer = BuildingBlockTemplateUpdateInputSerializer(
            data=request.data, instance=template, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        updated_template = building_block_template_update(existing_template=template, **serializer.validated_data)

        output_serializer = BuildingBlockTemplateDetailOutputSerializer(updated_template, context={"request": request})
        # Save data json in history to get easy history
        building_block_template_add_history(data=output_serializer.data, template=updated_template)

        return Response(output_serializer.data)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: BuildingBlockTemplateDetailOutputSerializer},
    )
    @action(detail=False, methods=["get"], url_path="empty_default")
    def get_empty_default(self, request):
        template = BuildingBlockTemplate.objects.get_empty_default()
        output_serializer = BuildingBlockTemplateDetailOutputSerializer(template, context={"request": request})

        return Response(output_serializer.data)

    @action(detail=True, methods=["post"])
    def request_publication(self, request, pk=None):
        template = self.get_object()

        template = building_block_template_request_publication(template=template)
        output_serializer = BuildingBlockTemplateDetailOutputSerializer(template, context={"request": request})
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def publish(self, request, pk=None):
        template = self.get_object()

        template = building_block_template_publish(template=template)
        output_serializer = BuildingBlockTemplateDetailOutputSerializer(template, context={"request": request})
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def unpublish(self, request, pk=None):
        template = self.get_object()

        template = building_block_template_unpublish(template=template)
        output_serializer = BuildingBlockTemplateDetailOutputSerializer(template, context={"request": request})
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: HistoryOutputSerializer},
    )
    @action(detail=True, methods=["get"])
    def history(self, request, pk=None):
        template = self.get_object()
        history = template.historic_data.all().order_by("-created_at")

        output_serializer = HistoryOutputSerializer(history, many=True)

        return Response(output_serializer.data)
