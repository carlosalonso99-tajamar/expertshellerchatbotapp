import os
import uuid
import json
from django.db import models
from django.conf import settings

def json_upload_path(instance, filename):
    return os.path.join("json-outputs", filename)  # Guardará en `openai_processing/json-outputs/`

class GeneratedJSON(models.Model):
    """
    Modelo para almacenar los JSON generados por OpenAI.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=json_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save_json(self, data):
        """
        Guarda el JSON en el sistema de archivos y almacena la referencia en la BD.
        """
        filename = f"{uuid.uuid4()}.json"
        file_path = os.path.join(settings.JSON_OUTPUTS_DIR, filename)

        # Guardar el JSON en un archivo
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        # Almacenar la referencia en la BD
        self.file.name = os.path.relpath(file_path, settings.BASE_DIR)  # Guardar la ruta relativa
        self.save()
