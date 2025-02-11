import os
from django.db import models
from django.conf import settings

def pdf_upload_path(instance, filename):
    return os.path.join("uploads", filename)  # Guardará en `ocr/uploads/`

class UploadedPDF(models.Model):
    """
    Modelo para almacenar PDFs subidos por los usuarios.
    """
    file = models.FileField(upload_to=pdf_upload_path)  # Guardar en `ocr/uploads/`
    extracted_text = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
