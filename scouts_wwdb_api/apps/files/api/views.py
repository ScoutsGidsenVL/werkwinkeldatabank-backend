import logging

from django.core.exceptions import ValidationError
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import permissions, serializers, status, views
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from ..models import CKEditorFile
from ..services.file_service import store_ckeditor_file
from .serializers import UploadFileInputSerializer, UploadFileOutputSerializer

logger = logging.getLogger(__name__)


class FileUploadView(views.APIView):
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        request_body=UploadFileInputSerializer,
        responses={status.HTTP_201_CREATED: UploadFileOutputSerializer},
    )
    def post(self, request):
        serializer = UploadFileInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        try:
            result = store_ckeditor_file(uploaded_file=data.get("upload"))
        except ValidationError as e:
            raise serializers.ValidationError("; ".join(e.messages))
        url = request.build_absolute_uri("/api/files/download/" + str(result.id))
        output_serializer = UploadFileOutputSerializer({"url": url, "id": str(result.id)})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class FileDownloadView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        ck_file = get_object_or_404(CKEditorFile.objects, pk=pk)
        logger.debug("CK FILE: %s", ck_file.file)
        return HttpResponse(ck_file.file, content_type=ck_file.content_type)
