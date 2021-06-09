from rest_framework import serializers
from apps.serializer_extensions.serializers import PermissionRequiredField


class DisabledFieldCreateInputSerializerMixin(metaclass=serializers.SerializerMetaclass):
    is_disabled = PermissionRequiredField(
        permission="scouts_auth.access_disabled_entities",
        field=serializers.BooleanField(default=False),
    )


class DisabledFieldUpdateInputSerializerMixin(metaclass=serializers.SerializerMetaclass):
    is_disabled = PermissionRequiredField(
        permission="scouts_auth.access_disabled_entities",
        field=serializers.BooleanField(required=False),
        required=False,
    )
