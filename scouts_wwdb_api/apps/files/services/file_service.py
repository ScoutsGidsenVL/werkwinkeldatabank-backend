from django.core.files.base import File

from ..models import CKEditorFile


def store_ckeditor_file(*, uploaded_file: File) -> CKEditorFile:
    ck_file = CKEditorFile()
    ck_file.file.save(name=uploaded_file.name, content=uploaded_file)
    ck_file.content_type = uploaded_file.content_type
    ck_file.full_clean()
    ck_file.save()

    return ck_file
