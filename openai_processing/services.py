import openai
import os
import json
from dotenv import load_dotenv
from .models import GeneratedJSON

load_dotenv()

openai_client = openai.AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2023-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

import re

class OpenAIService:
    @staticmethod
    def generate_structured_json(documents):
        """
        Envía los documentos a OpenAI y obtiene un JSON con intenciones y entidades detectadas automáticamente.
        """
        print("✅ Entrando en `generate_structured_json`")

        text_data = [{"filename": doc.file.name, "text": doc.extracted_text} for doc in documents]

        prompt = """
            Eres un experto en procesamiento de lenguaje natural (NLP) y comprensión de intenciones del usuario.
            Tu tarea es analizar los siguientes documentos y extraer automáticamente:
            1. **Intenciones (intents):** Lo que el usuario intenta lograr con el contenido.
            2. **Entidades (entities):** Datos clave mencionados en los documentos.
            3. **Utterances:** Frases de ejemplo que corresponden a cada intención y entidad.

            ### 📚 **Reglas generales**
            Genera un JSON estructurado siguiendo el formato de Conversational Language Understanding (CLU) de Azure.

            1️⃣ **Las entidades deben estar bien definidas en la sección 'entities' antes de usarlas en las utterances.**  
            2️⃣ **Cada utterance debe usar solo entidades previamente definidas en la lista de entidades.**  
            3️⃣ **El JSON debe incluir intenciones relevantes, entidades correctamente estructuradas y utterances que reflejen escenarios realistas.**  
            4️⃣ **No inventes entidades nuevas en las utterances si no han sido definidas previamente en la estructura del JSON.**  
            5️⃣ **Verifica que los valores de 'offset' y 'length' en cada utterance sean correctos y se correspondan con la posición exacta en la frase.**  
            6️⃣ **Si una entidad es mencionada en una utterance, debe estar correctamente definida en la lista de entidades.**  
            7️⃣ **Las intenciones deben ser útiles y reflejar acciones que un usuario realmente intentaría realizar.**

            
             ### 📌 **Reglas adicionales**
    - **No incluyas la clave `subentities` en las entidades.**  
    - **Si una entidad tiene componentes internos, usa la clave `children` en lugar de `subentities`.**
    - **Estructura correctamente las entidades siguiendo el formato de Azure CLU.**
            ---

            ### 📌 **Formato de salida requerido**
            Importante: **la salida debe ser solamente el JSON**.
            No incluyas explicaciones ni texto adicional antes o después del JSON.

            Ejemplo de formato:

            ```json
            {
                "projectFileVersion": "{API-VERSION}",
                "stringIndexType": "Utf16CodeUnit",
                "metadata": {
                    "projectKind": "Conversation",
                    "settings": {
                    "confidenceThreshold": 0.7
                    },
                    "projectName": "{PROJECT-NAME}",
                    "multilingual": true,
                    "description": "Trying out CLU",
                    "language": "{LANGUAGE-CODE}"
                },
                "assets": {
                    "projectKind": "Conversation",
                    "intents": [
                    {
                        "category": "intent1"
                    },
                    {
                        "category": "intent2"
                    }
                    ],
                    "entities": [
                    {
                        "category": "entity1"
                    }
                    ],
                    "utterances": [
                    {
                        "text": "text1",
                        "dataset": "{DATASET}",
                        "intent": "intent1",
                        "entities": [
                        {
                            "category": "entity1",
                            "offset": 5,
                            "length": 5
                        }
                        ]
                    },
                    {
                        "text": "text2",
                        "language": "{LANGUAGE-CODE}",
                        "dataset": "{DATASET}",
                        "intent": "intent2",
                        "entities": []
                    }
                    ]
                }
                }
            ```
        """


        try:
            print("📡 Enviando solicitud a OpenAI...")
            text_data_str = "\n".join([f"Documento: {doc['filename']}\nContenido:\n{doc['text']}" for doc in text_data])
            response = openai_client.chat.completions.create(
                model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
                messages=[
                    {"role": "system", "content": "Eres un asistente especializado en análisis de documentos."},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": text_data_str}
                ],
                max_tokens=1000
            )
            print("✅ Respuesta recibida de OpenAI")

            json_result = response.choices[0].message.content
            print(f"📜 JSON generado antes de limpieza:\n{json_result}")

            # Limpiar triple backticks y la palabra "json"
            json_result = re.sub(r"```json\n?|```", "", json_result).strip()
            print(f"📜 JSON después de limpieza:\n{json_result}")

            # Convertir a JSON válido
            parsed_json = json.loads(json_result)

            # Guardar en la BD y en el sistema de archivos
            json_instance = GeneratedJSON()
            json_instance.save_json(parsed_json)

            print("✅ JSON guardado en BD y archivos")
            return parsed_json
        except Exception as e:
            print(f"❌ Error en `generate_structured_json`: {e}")
            return {"error": str(e)}
