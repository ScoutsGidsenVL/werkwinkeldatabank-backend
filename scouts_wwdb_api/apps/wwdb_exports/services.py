"""apps.wwdb_exports.services."""
import logging
import os

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa

from apps.files.models import CKEditorFile
from apps.workshops.models import Workshop

logger = logging.getLogger(__name__)


def link_callback(uri, rel):
    # "http://localhost:8011/api/files/download/fd1c3746-841e-4d2c-a03e-d9abdd226701\"
    # Handle file links
    static_url = settings.STATIC_URL  # Typically /static/
    static_root = settings.STATIC_ROOT  # Typically /home/userX/project_static/

    logger.info("Received PISA callback for uri %s and rel %s", uri, rel)

    file_id = None
    if "/api/files/download/" in uri:
        file_id = uri.rpartition("/api/files/download/")[2].strip("\\ /")

        logger.info(f"Retrieving CKEditorFile instance with id {file_id}")
        ck_file = CKEditorFile.objects.get(pk=file_id)
        if not ck_file:
            raise Exception(f"Unable to retrieve CKEditorFile with id {file_id}")

        uri = ck_file.file.url

    elif static_url in uri:
        uri = os.path.join(static_root, uri.replace(static_url, ""))

    # https://stackoverflow.com/questions/2179958/django-pisa-adding-images-to-pdf-output
    logger.info(f"Returning file uri for CKEditorFile with id {file_id}: {uri}")

    return uri


def generate_pdf_response(*, template_path: str, context, filename: str) -> HttpResponse:
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = xhtml2pdf.pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisa_status.err:
        raise Exception(pisa_status.err)

    return response


def generate_workshop_pdf_response(*, workshop: Workshop) -> HttpResponse:
    context = {"workshop": workshop}
    filename = workshop.title.replace(" ", "_") + "_workshop.pdf"
    # return SimpleTemplateResponse(template="workshop.html", context=context)
    return generate_pdf_response(template_path="workshop.html", context=context, filename=filename)
