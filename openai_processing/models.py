import uuid
import os
import json
from django.db import models
from django.conf import settings

def json_upload_path(instance, filename):
    """Define la ruta donde se almacenarán los archivos JSON."""
    return os.path.join("json-outputs", filename)

class GeneratedJSON(models.Model):
    """
    Modelo que almacena los JSON generados por OpenAI.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=json_upload_path, blank=True, null=True)  # Guarda el JSON como archivo
    created_at = models.DateTimeField(auto_now_add=True)

    def save_json(self, data):
        """
        Guarda el JSON en un archivo y actualiza la referencia en el modelo.
        """
        json_filename = f"{self.id}.json"  # Genera un nombre único para el JSON
        json_path = os.path.join(settings.JSON_OUTPUTS_DIR, json_filename)  # Ruta completa

        try:
            with open(json_path, "w", encoding="utf-8") as json_file:
                json.dump(data, json_file, indent=4, ensure_ascii=False)

            self.file.name = os.path.join("json-outputs", json_filename)  # Guardar la ruta relativa en la BD
            self.save()
            print(f"✅ JSON guardado correctamente en {json_path}")

        except Exception as e:
            print(f"❌ Error guardando el JSON: {e}")

    def get_json(self):
        """
        Lee y devuelve el JSON almacenado en el archivo.
        """
        if self.file and os.path.exists(self.file.path):
            with open(self.file.path, "r", encoding="utf-8") as json_file:
                return json.load(json_file)
        return None

    def __str__(self):
        return f"JSON generado el {self.created_at}"
