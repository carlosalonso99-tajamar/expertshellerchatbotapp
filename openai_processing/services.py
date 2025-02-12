import openai
import os
import json
from dotenv import load_dotenv
from .models import GeneratedJSON

load_dotenv()

# Configurar el cliente OpenAI
openai_client = openai.OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

class OpenAIService:
    @staticmethod
    def extract_intents(documents):
        """ Extrae intenciones de los documentos en el formato esperado """
        prompt = """
        Analiza los siguientes documentos y extrae las intenciones principales en formato JSON estricto.
        Asegúrate de que las intenciones identificadas se referencien correctamente en las utterances.
        Formato:
        {
          "intents": [
            {"category": "intent1"},
            {"category": "intent2"}
          ]
        }
        """
        text_data = "\n".join([doc.extracted_text for doc in documents])
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "Eres un experto en NLP y clasificación de intenciones."},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": text_data}
                ],
                max_tokens=500
            )
            raw_response = response.choices[0].message.content.strip()
            raw_response = raw_response.replace("```json", "").replace("```", "").strip()
            return json.loads(raw_response)
        except json.JSONDecodeError as e:
            print(f"❌ Error al decodificar JSON en extract_intents: {e}")
            return {"intents": []}
    
    @staticmethod
    def extract_entities(documents):
        """ Extrae entidades en el formato esperado """
        prompt = """
        Analiza los siguientes documentos y extrae todas las entidades relevantes en formato JSON estricto.
        Asegúrate de que cada entidad identificada pueda ser referenciada en las utterances correctamente.
        Formato:
        {
          "entities": [
            {"category": "entity1"},
            {"category": "entity2"}
          ]
        }
        """
        text_data = "\n".join([doc.extracted_text for doc in documents])
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "Eres un experto en NLP y extracción de entidades."},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": text_data}
                ],
                max_tokens=500
            )
            raw_response = response.choices[0].message.content.strip()
            raw_response = raw_response.replace("```json", "").replace("```", "").strip()
            return json.loads(raw_response)
        except json.JSONDecodeError as e:
            print(f"❌ Error al decodificar JSON en extract_entities: {e}")
            return {"entities": []}
    
    @staticmethod
    def generate_utterances(documents, intents, entities):
        """ Genera ejemplos de utterances en el formato esperado """
        intents_json = json.dumps(intents, indent=2, ensure_ascii=False)
        entities_json = json.dumps(entities, indent=2, ensure_ascii=False)
        
        prompt = f"""
        Basado en las siguientes intenciones y entidades, genera ejemplos de utterances en formato JSON estricto.
        Asegúrate de que cada utterance tenga un intent referenciado correctamente en la lista de intents y que las entidades existan en la lista de entities.
        Formato:
        {{
          "utterances": [
            {{
              "text": "utterance1",
              "intent": "intent1",
              "language": "es",
              "dataset": "Train",
              "entities": [
                {{
                  "category": "entity1",
                  "offset": 6,
                  "length": 4
                }}
              ]
            }}
          ]
        }}
        
        Intenciones detectadas: {intents_json}
        Entidades detectadas: {entities_json}
        """
        
        text_data = "\n".join([doc.extracted_text for doc in documents])
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "Eres un experto en NLP y generación de ejemplos de conversación."},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": text_data}
                ],
                max_tokens=1000
            )
            raw_response = response.choices[0].message.content.strip()
            raw_response = raw_response.replace("```json", "").replace("```", "").strip()
            return json.loads(raw_response)
        except json.JSONDecodeError as e:
            print(f"❌ Error al decodificar JSON en generate_utterances: {e}")
            return {"utterances": []}
    
    @staticmethod
    def generate_structured_json(documents):
        """ Ensambla el JSON final """
        print("✅ Extrayendo intenciones...")
        intents = OpenAIService.extract_intents(documents)
        print("✅ Extrayendo entidades...")
        entities = OpenAIService.extract_entities(documents)
        print("✅ Generando utterances...")
        utterances = OpenAIService.generate_utterances(documents, intents, entities)
        
        final_json = {
            "projectFileVersion": "2023-04-01",
            "stringIndexType": "Utf16CodeUnit",
            "metadata": {
                "projectKind": "Conversation",
                "projectName": "PRODUCTS-PROJECT",
                "multilingual": True,
                "description": "DESCRIPTION",
                "language": "es",
                "settings": {"confidenceThreshold": 0.7 }
            },
            "assets": {
                "projectKind": "Conversation",
                "intents": intents["intents"],
                "entities": entities["entities"],
                "utterances": utterances["utterances"]
            }
        }
        
        json_instance = GeneratedJSON()
        json_instance.save_json(final_json)
        
        print("✅ JSON estructurado generado y guardado correctamente.")
        return final_json
