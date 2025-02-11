import uuid
from django.db import models
from openai_processing.models import GeneratedJSON
from ocr.models import UploadedPDF

class Project(models.Model):
    """
    Modelo que representa un proyecto basado en los JSON generados.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    json_file = models.OneToOneField(GeneratedJSON, on_delete=models.SET_NULL, null=True, blank=True, related_name="project")
    documents = models.ManyToManyField(UploadedPDF, related_name="projects")
    azure_project_id = models.CharField(max_length=255, blank=True, null=True)  # ID en Azure

    def __str__(self):
        return self.name
