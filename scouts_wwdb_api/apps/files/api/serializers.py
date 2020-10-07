from rest_framework import serializers


class UploadFileInputSerializer(serializers.Serializer):
    upload = serializers.FileField()


class UploadFileOutputSerializer(serializers.Serializer):
    url = serializers.CharField()
