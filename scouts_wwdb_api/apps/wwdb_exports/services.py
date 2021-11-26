import logging, os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from apps.workshops.models import Workshop
from apps.files.models import CKEditorFile


logger = logging.getLogger(__name__)


def link_callback(uri, rel):
    # "http://localhost:8011/api/files/download/fd1c3746-841e-4d2c-a03e-d9abdd226701\"
    # Handle file links
    sUrl = settings.STATIC_URL  # Typically /static/
    sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/

    logger.debug("Received PISA callback for uri %s and rel %s", uri, rel)

    if "/api/files/download/" in uri:
        file_id = uri.rpartition("/api/files/download/")[2].strip("\\ /")

        logger.debug("Retrieving CKEditorFile instance with id %s", file_id)
        ck_file = CKEditorFile.objects.get(pk=file_id)
        if not ck_file:
            raise Exception("Unable to retrieve CKEditorFile with id {}".format(file_id))

        uri = ck_file.file.url
    elif sUrl in uri:
        uri = os.path.join(sRoot, uri.replace(sUrl, ""))

    # https://stackoverflow.com/questions/2179958/django-pisa-adding-images-to-pdf-output
    logger.debug("Returning file uri for CKEditorFile with id %s: %s", file_id, uri)

    return uri


def generate_pdf_response(*, template_path: str, context, filename: str) -> HttpResponse:
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="%s"' % filename

    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
        raise Exception(pisaStatus.err)

    return response


def generate_workshop_pdf_response(*, workshop: Workshop) -> HttpResponse:
    context = {"workshop": workshop}
    filename = workshop.title.replace(" ", "_") + "_workshop.pdf"
    # return SimpleTemplateResponse(template="workshop.html", context=context)
    return generate_pdf_response(template_path="workshop.html", context=context, filename=filename)
