from django.urls import path
from .api.views import FileUploadView, FileDownloadView

urlpatterns = [
    path("upload/", FileUploadView.as_view()),
    path("download/<str:pk>", FileDownloadView.as_view()),
]
