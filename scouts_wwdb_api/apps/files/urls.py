"""apps.files.urls."""
from django.urls import path

from apps.files.api.views import FileDownloadView, FileUploadView

urlpatterns = [
    path("upload/", FileUploadView.as_view()),
    path("download/<str:pk>", FileDownloadView.as_view()),
]
