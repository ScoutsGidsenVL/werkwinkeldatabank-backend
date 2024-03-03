from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from ..models import CKEditorFile


class UploadFileInputSerializer(serializers.Serializer):
    upload = serializers.FileField()


class UploadFileOutputSerializer(serializers.Serializer):
    id = serializers.CharField()
    url = serializers.CharField()


class FileDetailOutputSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()

    class Meta:
        model = CKEditorFile
        fields = (
            "id",
            "content_type",
            "name",
            "size",
        )

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_name(self, CKEditorFile):
        if CKEditorFile.file.name:
            return CKEditorFile.file.name
        else:
            return None

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_size(self, CKEditorFile):
        if CKEditorFile.file.size:
            return CKEditorFile.file.size
        else:
            return None
