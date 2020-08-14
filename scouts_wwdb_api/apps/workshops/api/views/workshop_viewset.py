from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from ..serializers.workshop_serializers import (
    WorkshopDetailOutputSerializer,
    WorkshopListOutputSerializer,
    WorkshopCreateInputSerializer,
    WorkshopUpdateInputSerializer,
)
from ...services.workshop_service import workshop_create, workshop_update
from ...models import Workshop
from pprint import pprint
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter


class WorkshopViewSet(viewsets.GenericViewSet):
    filter_backends = [SearchFilter]
    search_fields = ["title", "workshop__title"]

    def get_queryset(self):
        """ queryset = Workshop.objects.all()
        workshop_title = self.request.query_params.get("title", None)
        if workshop_title is not None:
            queryset = queryset.filter(workshop__title=username)
        return queryset """
        return Workshop.objects.all()

    @swagger_auto_schema(responses={status.HTTP_200_OK: WorkshopDetailOutputSerializer})
    def retrieve(self, request, pk=None):
        workshop = get_object_or_404(Workshop.objects, pk=pk)
        pprint(workshop.theme)
        serializer = WorkshopDetailOutputSerializer(workshop)

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=WorkshopCreateInputSerializer, responses={status.HTTP_201_CREATED: WorkshopDetailOutputSerializer}
    )
    def create(self, request):
        input_serializer = WorkshopCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        created_workshop = workshop_create(**input_serializer.validated_data)

        output_serializer = WorkshopDetailOutputSerializer(created_workshop)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: WorkshopListOutputSerializer})
    def list(self, request):
        workshops = self.get_queryset()
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
        workshop = get_object_or_404(Workshop.objects, pk=pk)

        serializer = WorkshopUpdateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_workshop = workshop_update(existing_workshop=workshop, **serializer.validated_data)

        output_serializer = WorkshopDetailOutputSerializer(updated_workshop)

        return Response(output_serializer.data)
