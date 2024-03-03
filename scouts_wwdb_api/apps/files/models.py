from django.core.validators import FileExtensionValidator
from django.db import models

from apps.base.models import BaseModel
from apps.workshops.models import Workshop


class CKEditorFile(BaseModel):
    file = models.FileField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "gif", "bmp", "webp", "tiff", "odt", "pptx", "docx", "pdf"]
            )
        ]
    )
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, blank=True, null=True, related_name="files")
    content_type = models.CharField(max_length=100)
