from django.urls import path
from .views import document_context, process_texts, list_json_files

app_name = "openai_processing"


urlpatterns = [
    path("document-context/", document_context, name="document_context"),
    path("process-texts/", process_texts, name="process_texts"),
    path("json-files/", list_json_files, name="json-files"),
]
