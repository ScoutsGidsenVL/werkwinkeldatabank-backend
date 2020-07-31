from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..serializers.workshop_serializers import WorkshopDetailOutputSerializer
from ...models import Workshop

class WorkshopViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        workshop = get_object_or_404(Workshop.objects, pk=pk)
        serializer = WorkshopDetailOutputSerializer(theme)

        return Response(serializer.data)