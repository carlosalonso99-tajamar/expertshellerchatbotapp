import os
import requests
from django.conf import settings
from .models import Project

AZURE_CONVERSATIONAL_API_URL = "https://<your-azure-resource>.cognitiveservices.azure.com/language/conversation/projects"

class AzureProjectService:
    @staticmethod
    def create_project_in_azure(project: Project):
        """
        Envía el JSON del proyecto a Azure Conversational Language Services.
        """
        headers = {
            "Ocp-Apim-Subscription-Key": os.getenv("AZURE_CONVERSATIONAL_KEY"),
            "Content-Type": "application/json",
        }

        with open(project.json_file.file.path, "r", encoding="utf-8") as f:
            json_data = f.read()

        response = requests.post(AZURE_CONVERSATIONAL_API_URL, headers=headers, data=json_data)

        if response.status_code == 200:
            project.azure_project_id = response.json().get("id")
            project.save()
            return {"success": True, "message": "Proyecto creado en Azure", "azure_id": project.azure_project_id}
        else:
            return {"success": False, "error": response.text}
