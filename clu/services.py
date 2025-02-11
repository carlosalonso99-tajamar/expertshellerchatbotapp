import os
import requests
from dotenv import load_dotenv

load_dotenv()

class CLUService:
    @staticmethod
    def create_clu_project(name, description, json_data):
        """
        Crea un nuevo proyecto en Azure CLU utilizando el JSON generado.
        """
        endpoint = "https://carlos-ai-lang.cognitiveservices.azure.com/"
        api_key = "viUVh1sjdzBWKmyGJnmCNlECpmYQFhimn1dxE7U7tsBBlkd1pO8RJQQJ99BBACYeBjFXJ3w3AAAaACOGrbJX"
        api_version = "2023-04-01"

        url = f"{endpoint}/language/authoring/analyze-conversations/projects/{name}/:import?api-version={api_version}"

        headers = {
            "Ocp-Apim-Subscription-Key": api_key,
            "Content-Type": "application/json",
            "Cache-Control": "no-cache"
        }

        # #cambiar el nombre yy la descripcion en el json data y reflejarlo en el json real
        json_data["metadata"]["projectName"] = name
        json_data["metadata"]["description"] = description
        json_data["projectFileVersion"] = api_version
        print(json_data)
        
        json_payload = json_data

        print(f"📡 Enviando solicitud a Azure CLU para crear el proyecto {name}...")

        response = requests.post(url, headers=headers, json=json_payload)

        if response.status_code in [200, 201]:
            print(f"✅ Proyecto {name} creado con éxito en Azure CLU.")
            return response.json()
        elif response.status_code == 202:
            # Verificar si la respuesta contiene la URL del trabajo en progreso
            operation_location = response.headers.get("operation-location")

            if operation_location:
                print(f"📡 La importación está en progreso. Monitoreando en: {operation_location}")
            else:
                print("❌ No se encontró la URL de seguimiento en la respuesta.")
    
        else:
            print(f"❌ Error en la creación del proyecto en Azure CLU: {response.status_code}")
            print(f"📝 Respuesta de Azure: {response}")
            return {"error": response.text}
