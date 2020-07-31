from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..serializers.workshop_serializers import WorkshopDetailOutputSerializer, WorkshopListOutputSerializer, WorkshopCreateInputSerializer, WorkshopUpdateInputSerializer
from ...services.workshop_service import workshop_create
from ...models import Workshop

class WorkshopViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        workshop = get_object_or_404(Workshop.objects, pk=pk)
        serializer = WorkshopDetailOutputSerializer(theme)

        return Response(serializer.data)

    def create(self, request):
        input_serializer = WorkshopCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        created_theme = workshop_create(**input_serializer.validated_data)

        output_serializer = ThemeDetailOutputSerializer(created_theme)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        workshops = Workshop.objects.all()
        serializer = WorkshopListOutputSerializer(workshops, many=True)

        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        workshop = get_object_or_404(Workshop.objects, pk=pk)
        serializer = WorkshopUpdateInputSerializer(workshop)

        return Response(serializer.data)
