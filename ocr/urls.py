from django.urls import path
from .views import upload_documents

app_name = "ocr"

urlpatterns = [
    path("upload-documents/<uuid:project_id>/", upload_documents, name="upload"),
]

