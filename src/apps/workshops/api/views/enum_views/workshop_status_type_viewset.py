from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from ....models.enums.workshop_status_type import WorkshopStatusType
from ...serializers.enum_serializers import EnumOutputSerializer


class WorkshopStatusTypeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumOutputSerializer})
    def list(self, request):
        serializer = EnumOutputSerializer(WorkshopStatusType.choices, many=True)
        return Response(serializer.data)
