from rest_framework import viewsets, status, serializers, filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import F
from rest_framework.exceptions import APIException
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from ..serializers.workshop_serializers import (
    WorkshopDetailOutputSerializer,
    WorkshopListOutputSerializer,
    WorkshopCreateInputSerializer,
    WorkshopUpdateInputSerializer,
)
from ..serializers.history_serializers import HistoryOutputSerializer
from ...services.workshop_service import (
    workshop_create,
    workshop_update,
    workshop_request_publication,
    workshop_publish,
    workshop_unpublish,
    workshop_add_history,
)
from ...models import Workshop
from ...models.enums.workshop_status_type import WorkshopStatusType
from ..filters.workshop_filter import WorkshopFilter
from ...exceptions import InvalidWorkflowTransitionException
from ..exceptions import InvalidWorkflowTransitionAPIException
from ..permissions.custom_django_permission import CustomDjangoPermission
from functools import partial


class WorkshopViewSet(viewsets.GenericViewSet):
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = WorkshopFilter
    ordering_fields = ["published_at", "created_at"]
    ordering = [F("published_at").desc(nulls_last=True), "-created_at"]

    def get_queryset(self):
        return Workshop.objects.all().allowed(self.request.user)

    def get_serializer_class(self):
        return WorkshopDetailOutputSerializer

    def handle_exception(self, exc):
        if isinstance(exc, InvalidWorkflowTransitionException):
            exc = InvalidWorkflowTransitionAPIException(exc)

        return super().handle_exception(exc)

    @swagger_auto_schema(responses={status.HTTP_200_OK: WorkshopDetailOutputSerializer})
    def retrieve(self, request, pk=None):
        workshop = get_object_or_404(Workshop.objects, pk=pk)
        serializer = WorkshopDetailOutputSerializer(workshop)

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=WorkshopCreateInputSerializer, responses={status.HTTP_201_CREATED: WorkshopDetailOutputSerializer}
    )
    def create(self, request):
        input_serializer = WorkshopCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        created_workshop = workshop_create(**input_serializer.validated_data, created_by=request.user)

        output_serializer = WorkshopDetailOutputSerializer(created_workshop)
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
            serializer = WorkshopListOutputSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = WorkshopListOutputSerializer(workshops, many=True)
            return Response(serializer.data)

    @swagger_auto_schema(
        request_body=WorkshopUpdateInputSerializer, responses={status.HTTP_200_OK: WorkshopDetailOutputSerializer}
    )
    def partial_update(self, request, pk=None):
        workshop = get_object_or_404(self.get_queryset(), pk=pk)

        serializer = WorkshopUpdateInputSerializer(data=request.data, instance=workshop, context={"request": request})
        serializer.is_valid(raise_exception=True)

        updated_workshop = workshop_update(existing_workshop=workshop, **serializer.validated_data)

        output_serializer = WorkshopDetailOutputSerializer(updated_workshop)
        # Save data json in history to get easy history
        workshop_add_history(data=output_serializer.data, workshop=updated_workshop)

        return Response(output_serializer.data)

    @action(detail=True, methods=["post"])
    def request_publication(self, request, pk=None):
        workshop = get_object_or_404(self.get_queryset(), pk=pk)

        updated_workshop = workshop_request_publication(workshop=workshop)
        output_serializer = WorkshopDetailOutputSerializer(updated_workshop)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def publish(self, request, pk=None):
        workshop = get_object_or_404(self.get_queryset(), pk=pk)

        updated_workshop = workshop_publish(workshop=workshop)
        output_serializer = WorkshopDetailOutputSerializer(updated_workshop)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def unpublish(self, request, pk=None):
        workshop = get_object_or_404(self.get_queryset(), pk=pk)

        updated_workshop = workshop_unpublish(workshop=workshop)
        output_serializer = WorkshopDetailOutputSerializer(updated_workshop)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def published_workshops(self, request):
        # Apply filter using the custom manager
        workshops = self.filter_queryset(self.get_queryset().published())
        # Apply paging
        page = self.paginate_queryset(workshops)

        if page is not None:
            serializer = WorkshopListOutputSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = WorkshopListOutputSerializer(workshops, many=True)
            return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def my_workshops(self, request):
        # Apply filter using the custom manager
        workshops = self.filter_queryset(self.get_queryset().owned(request.user.id))
        # Apply paging
        page = self.paginate_queryset(workshops)

        if page is not None:
            serializer = WorkshopListOutputSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = WorkshopListOutputSerializer(workshops, many=True)
            return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[partial(CustomDjangoPermission, "workshops.view_to_be_published_workshops2")],
    )
    def publication_requested_workshops(self, request):
        # Apply filter using the custom manager
        workshops = self.filter_queryset(self.get_queryset().publication_requested())
        # Apply paging
        page = self.paginate_queryset(workshops)

        if page is not None:
            serializer = WorkshopListOutputSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = WorkshopListOutputSerializer(workshops, many=True)
            return Response(serializer.data)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: HistoryOutputSerializer},
    )
    @action(detail=True, methods=["get"])
    def history(self, request, pk=None):
        workshop = get_object_or_404(self.get_queryset(), pk=pk)
        history = workshop.historic_data.all().order_by("-created_at")

        output_serializer = HistoryOutputSerializer(history, many=True)

        return Response(output_serializer.data)
