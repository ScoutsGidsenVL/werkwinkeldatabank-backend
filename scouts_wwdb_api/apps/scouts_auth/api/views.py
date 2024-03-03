from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views
from rest_framework.response import Response

from .serializers import UserDetailOutputSerializer


class CurrentUserView(views.APIView):
    @swagger_auto_schema(responses={status.HTTP_200_OK: UserDetailOutputSerializer})
    def get(self, request):
        output_serializer = UserDetailOutputSerializer(request.user)

        return Response(output_serializer.data)
