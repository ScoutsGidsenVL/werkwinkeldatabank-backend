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
from ...services.workshop_service import workshop_create
from ...models import Workshop


class WorkshopViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={status.HTTP_200_OK: WorkshopDetailOutputSerializer})
    def retrieve(self, request, pk=None):
        workshop = get_object_or_404(Workshop.objects, pk=pk)
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
        workshops = Workshop.objects.all()
        serializer = WorkshopListOutputSerializer(workshops, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=WorkshopUpdateInputSerializer, responses={status.HTTP_200_OK: WorkshopDetailOutputSerializer}
    )
    def partial_update(self, request, pk=None):
        workshop = get_object_or_404(Workshop.objects, pk=pk)
        serializer = WorkshopUpdateInputSerializer(workshop)

        return Response(serializer.data)
