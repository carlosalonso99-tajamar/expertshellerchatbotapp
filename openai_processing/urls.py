from django.urls import path
from .views import list_json_files#, process_texts # document_context, 

app_name = "openai_processing"


urlpatterns = [
    # path("document-context/", document_context, name="document_context"),
    path("json-files/", list_json_files, name="json-files"),
]
