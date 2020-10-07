from django.db import models
from django.core.validators import FileExtensionValidator
from apps.base.models import BaseModel


class CKEditorFile(BaseModel):
    file = models.FileField(
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "gif", "bmp", "webp", "tiff"])]
    )
    content_type = models.CharField(max_length=100)
