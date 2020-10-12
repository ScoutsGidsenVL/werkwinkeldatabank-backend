import copy
import inspect
from rest_framework import serializers
from rest_framework.fields import empty
from drf_yasg import openapi
from pprint import pprint

# Overwrite DurationField to give it correct swagger configuration
class DurationField(serializers.DurationField):
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_STRING,
            "format": "[DD] [HH:[MM:]]ss[.uuuuuu]",
        }


# Custom field that only parses value if you have the required permission
class PermissionRequiredInputField(serializers.Field):
    field = None
    permission = None

    def __init__(self, *args, **kwargs):
        self.field = kwargs.pop("field", copy.deepcopy(self.field))
        self.permission = kwargs.pop("permission")
        assert self.field is not None, "`field` is a required argument."
        assert not inspect.isclass(self.field), "`field` has not been instantiated."
        assert self.permission is not None, "`permission` is a required argument."
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        request = self.context.get("request")
        if not request:
            raise Exception(
                "Make sure request has been given to the context of the serializer,"
                "otherwise PermissionRequiredField won't work"
            )
        # If have permission just act as if you are the given field with data
        if request.user.has_perm(self.permission):
            return self.field.run_validation(data)
        # Else act as if no value given
        return self.field.run_validation(empty)


# Create serializer field that can switch between a create and a delete depending on id given
# Usefull for nested models in input serializers
class SerializerSwitchField(serializers.Field):
    create_serializer = None
    update_serializer = None

    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "description": (
                "Exact documentation not available, look at corresponding POST for this model to see possible fields."
                "If you want to update an existing entity make sure to also give id as field in this object"
            ),
        }

    def __init__(self, *args, **kwargs):
        self.create_serializer = kwargs.pop("create_serializer", copy.deepcopy(self.create_serializer))
        self.update_serializer = kwargs.pop("update_serializer", copy.deepcopy(self.update_serializer))
        assert self.create_serializer is not None, "`create_serializer` is a required argument."
        assert not inspect.isclass(self.create_serializer), "`create_serializer` has not been instantiated."
        assert self.update_serializer is not None, "`update_serializer` is a required argument."
        assert not inspect.isclass(self.update_serializer), "`update_serializer` has not been instantiated."
        super().__init__(*args, **kwargs)
        self.create_serializer.bind(field_name="", parent=self)
        self.update_serializer.bind(field_name="", parent=self)

    def to_internal_value(self, data):
        if data.get("id", None):
            return self.update_serializer.run_validation(data)
        else:
            return self.create_serializer.run_validation(data)
