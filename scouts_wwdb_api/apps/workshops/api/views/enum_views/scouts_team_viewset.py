from drf_yasg2.utils import swagger_auto_schema
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from ....models.enums.scouts_team import ScoutsTeam
from ...serializers.enum_serializers import EnumOutputSerializer


class ScoutsTeamViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumOutputSerializer})
    def list(self, request):
        serializer = EnumOutputSerializer(ScoutsTeam.choices, many=True)
        return Response(serializer.data)
