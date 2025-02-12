import os
import requests
from dotenv import load_dotenv


class CLUService:
    @staticmethod
    def create_clu_project(name, description, json_data):
        """
        Crea un nuevo proyecto en Azure CLU utilizando el JSON generado.
        """
        load_dotenv()

        endpoint =  os.getenv("AZURE_CLU_ENDPOINT")
        api_key =  os.getenv("AZURE_CLU_API_KEY")
        api_version = "2023-04-01"

        print("Endpoint", endpoint)
        print("Key", api_key)
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
        
        json_payload = CLUJSONValidator.validate_and_fix(json_data)

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

import json

class CLUJSONValidator:
    @staticmethod
    def validate_and_fix(json_data):
        """
        Valida y corrige errores en el JSON de CLU generado por OpenAI.
        """
        print("🔍 Validando JSON...")

        # 1️⃣ **Eliminar la clave `children` de las entidades**
        if "assets" in json_data and "entities" in json_data["assets"]:
            for entity in json_data["assets"]["entities"]:
                if "children" in entity:
                    del entity["children"]

        # 2️⃣ **Corregir `dataset` (default → Train)**
        valid_datasets = {"Train", "Test"}
        if "assets" in json_data and "utterances" in json_data["assets"]:
            for utterance in json_data["assets"]["utterances"]:
                if "dataset" in utterance and utterance["dataset"] not in valid_datasets:
                    print(f"⚠ Dataset incorrecto en: {utterance['text']} -> Se asignará 'Train'")
                    utterance["dataset"] = "Train"  # Asigna Train por defecto

        # 3️⃣ **Corregir offsets y lengths en entidades**
        for utterance in json_data["assets"]["utterances"]:
            text_length = len(utterance["text"])
            if "entities" in utterance:
                for entity in utterance["entities"]:
                    offset = entity.get("offset", 0)
                    length = entity.get("length", 0)

                    # Ajustar offset si es mayor que la longitud del texto
                    if offset >= text_length:
                        print(f"⚠ Offset fuera de rango en: {utterance['text']} -> Se ajusta a 0")
                        entity["offset"] = 0  # Se reubica al inicio

                    # Ajustar length si supera los límites
                    if offset + length > text_length:
                        new_length = text_length - offset
                        print(f"⚠ Longitud incorrecta en: {utterance['text']} -> Se ajusta de {length} a {new_length}")
                        entity["length"] = new_length

        print("✅ Validación y corrección completadas.")
        return json_data

