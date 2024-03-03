from functools import partial

from django.core.exceptions import PermissionDenied
from django.db.models import F
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from apps.scouts_auth.permissions import CustomDjangoPermission, ExtendedDjangoModelPermissions
from apps.wwdb_exports.services import generate_workshop_pdf_response

from ...exceptions import InvalidWorkflowTransitionException
from ...models import Workshop
from ...models.enums.workshop_status_type import WorkshopStatusType
from ...services.workshop_service import (
    workshop_add_history,
    workshop_create,
    workshop_publish,
    workshop_request_publication,
    workshop_unpublish,
    workshop_update,
)
from ..exceptions import InvalidWorkflowTransitionAPIException
from ..filters.workshop_filter import WorkshopFilter
from ..permissions import WorkshopChangePermission
from ..serializers.history_serializers import HistoryOutputSerializer
from ..serializers.workshop_serializers import (
    WorkshopCreateInputSerializer,
    WorkshopDetailOutputSerializer,
    WorkshopListOutputSerializer,
    WorkshopUpdateInputSerializer,
)


class WorkshopViewSet(viewsets.GenericViewSet):
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = WorkshopFilter
    ordering_fields = ["published_at", "created_at"]
    ordering = [F("published_at").desc(nulls_last=True), "-created_at"]
    permission_classes = [ExtendedDjangoModelPermissions]

    def get_queryset(self):
        return Workshop.objects.all().allowed(self.request.user)

    def get_serializer_class(self):
        return WorkshopDetailOutputSerializer

    def get_permissions(self):
        current_permissions = super().get_permissions()
        if self.action in ("retrieve", "list", "published_workshops", "download"):
            return [permissions.AllowAny()]
        if self.action == "history":
            current_permissions.append(CustomDjangoPermission("workshops.view_history"))
        if self.action == "partial_update":
            current_permissions.append(WorkshopChangePermission())
        if self.action == "request_publication":
            current_permissions.extend(
                [CustomDjangoPermission("workshops.request_publication_workshop"), WorkshopChangePermission()]
            )
        if self.action == "publish":
            current_permissions.append(CustomDjangoPermission("workshops.publish_workshop"))
        if self.action == "unpublish":
            current_permissions.append(CustomDjangoPermission("workshops.unpublish_workshop"))

        return current_permissions

    def handle_exception(self, exc):
        if isinstance(exc, InvalidWorkflowTransitionException):
            exc = InvalidWorkflowTransitionAPIException(exc)

        return super().handle_exception(exc)

    @swagger_auto_schema(responses={status.HTTP_200_OK: WorkshopDetailOutputSerializer})
    def retrieve(self, request, pk=None):
        workshop = self.get_object()
        serializer = WorkshopDetailOutputSerializer(workshop, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=WorkshopCreateInputSerializer, responses={status.HTTP_201_CREATED: WorkshopDetailOutputSerializer}
    )
    def create(self, request):
        input_serializer = WorkshopCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        created_workshop = workshop_create(**input_serializer.validated_data, created_by=request.user)

        output_serializer = WorkshopDetailOutputSerializer(created_workshop, context={"request": request})
        # Save data json in history to get easy history
        workshop_add_history(data=output_serializer.data, workshop=created_workshop)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: WorkshopListOutputSerializer})
    def list(self, request):
        # Apply filters
        workshops = self.filter_queryset(self.get_queryset())
        # Apply paging
        page = self.paginate_queryset(workshops)

        if page is not None:
            serializer = WorkshopListOutputSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        else:
            serializer = WorkshopListOutputSerializer(workshops, many=True, context={"request": request})
            return Response(serializer.data)

    @swagger_auto_schema(
        request_body=WorkshopUpdateInputSerializer, responses={status.HTTP_200_OK: WorkshopDetailOutputSerializer}
    )
    def partial_update(self, request, pk=None):
        workshop = self.get_object()

        serializer = WorkshopUpdateInputSerializer(data=request.data, instance=workshop, context={"request": request})
        serializer.is_valid(raise_exception=True)

        updated_workshop = workshop_update(existing_workshop=workshop, **serializer.validated_data)

        output_serializer = WorkshopDetailOutputSerializer(updated_workshop, context={"request": request})
        # Save data json in history to get easy history
        workshop_add_history(data=output_serializer.data, workshop=updated_workshop)

        return Response(output_serializer.data)

    @action(detail=True, methods=["post"])
    def request_publication(self, request, pk=None):
        workshop = self.get_object()

        updated_workshop = workshop_request_publication(workshop=workshop)
        output_serializer = WorkshopDetailOutputSerializer(updated_workshop, context={"request": request})
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def publish(self, request, pk=None):
        workshop = self.get_object()

        updated_workshop = workshop_publish(workshop=workshop)
        output_serializer = WorkshopDetailOutputSerializer(updated_workshop, context={"request": request})
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def unpublish(self, request, pk=None):
        workshop = self.get_object()

        updated_workshop = workshop_unpublish(workshop=workshop)
        output_serializer = WorkshopDetailOutputSerializer(updated_workshop, context={"request": request})
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def published_workshops(self, request):
        # Apply filter using the custom manager
        workshops = self.filter_queryset(self.get_queryset().published())
        # Apply paging
        page = self.paginate_queryset(workshops)

        if page is not None:
            serializer = WorkshopListOutputSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        else:
            serializer = WorkshopListOutputSerializer(workshops, many=True, context={"request": request})
            return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def my_workshops(self, request):
        # Apply filter using the custom manager
        workshops = self.filter_queryset(self.get_queryset().owned(request.user))
        # Apply paging
        page = self.paginate_queryset(workshops)

        if page is not None:
            serializer = WorkshopListOutputSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        else:
            serializer = WorkshopListOutputSerializer(workshops, many=True, context={"request": request})
            return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def publication_requested_workshops(self, request):
        # Apply filter using the custom manager
        workshops = self.filter_queryset(self.get_queryset().publication_requested())
        # Apply paging
        page = self.paginate_queryset(workshops)

        if page is not None:
            serializer = WorkshopListOutputSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        else:
            serializer = WorkshopListOutputSerializer(workshops, many=True, context={"request": request})
            return Response(serializer.data)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: HistoryOutputSerializer},
    )
    @action(detail=True, methods=["get"])
    def history(self, request, pk=None):
        workshop = self.get_object()
        history = workshop.historic_data.all().order_by("-created_at")

        output_serializer = HistoryOutputSerializer(history, many=True)

        return Response(output_serializer.data)

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None):
        workshop = self.get_object()
        return generate_workshop_pdf_response(workshop=workshop)
