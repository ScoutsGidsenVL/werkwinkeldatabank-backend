from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import APIException
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from ..serializers.workshop_serializers import (
    WorkshopDetailOutputSerializer,
    WorkshopListOutputSerializer,
    WorkshopCreateInputSerializer,
    WorkshopUpdateInputSerializer,
)
from ...services.workshop_service import workshop_create, workshop_update, workshop_status_change
from ...models import Workshop
from ...models.enums.workshop_status_type import WorkshopStatusType
from ..filters.workshop_filter import WorkshopFilter
from pprint import pprint
from ..exceptions import InvalidWorkflowTransitionException


class WorkshopViewSet(viewsets.GenericViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = WorkshopFilter

    def get_queryset(self):
        return Workshop.objects.all().allowed(self.request.user)

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

        return Response(output_serializer.data)

    @action(detail=True, methods=["post"])
    def request_publication(self, request, pk=None):
        workshop = get_object_or_404(self.get_queryset(), pk=pk)
        status_type = WorkshopStatusType.PUBLICATION_REQUESTED

        if workshop.workshop_status_type == WorkshopStatusType.PRIVATE:
            updated_workshop = workshop_status_change(existing_workshop=workshop, workshop_status=status_type)
            output_serializer = WorkshopDetailOutputSerializer(updated_workshop)
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        else:
            raise InvalidWorkflowTransitionException(from_msg=workshop.workshop_status_type, to_msg=status_type)

    @action(detail=True, methods=["post"])
    def publish(self, request, pk=None):
        workshop = get_object_or_404(self.get_queryset(), pk=pk)
        status_type = WorkshopStatusType.PUBLISHED

        if workshop.workshop_status_type == WorkshopStatusType.PUBLICATION_REQUESTED:
            if not workshop.approving_team:
                raise serializers.ValidationError("A workshop needs an approving team before it can be published")
            updated_workshop = workshop_status_change(existing_workshop=workshop, workshop_status=status_type)
            output_serializer = WorkshopDetailOutputSerializer(updated_workshop)
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        else:
            raise InvalidWorkflowTransitionException(from_msg=workshop.workshop_status_type, to_msg=status_type)

    @action(detail=True, methods=["post"])
    def unpublish(self, request, pk=None):
        workshop = get_object_or_404(self.get_queryset(), pk=pk)
        status_type = WorkshopStatusType.PRIVATE

        if workshop.workshop_status_type == WorkshopStatusType.PUBLISHED:
            updated_workshop = workshop_status_change(existing_workshop=workshop, workshop_status=status_type)
            output_serializer = WorkshopDetailOutputSerializer(updated_workshop)
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        else:
            raise InvalidWorkflowTransitionException(from_msg=workshop.workshop_status_type, to_msg=status_type)

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

    @action(detail=False, methods=["get"])
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
