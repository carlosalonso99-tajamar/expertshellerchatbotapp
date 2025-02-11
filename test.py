import requests
import time

# Configuración del recurso
API_KEY = "viUVh1sjdzBWKmyGJnmCNlECpmYQFhimn1dxE7U7tsBBlkd1pO8RJQQJ99BBACYeBjFXJ3w3AAAaACOGrbJX"
ENDPOINT = "https://carlos-ai-lang.cognitiveservices.azure.com/"
PROJECT_NAME = "4"
API_VERSION = "2023-04-01"

# URL para importar el proyecto
url = f"{ENDPOINT}/language/authoring/analyze-conversations/projects/{PROJECT_NAME}/:import?api-version={API_VERSION}"

# Encabezados de la solicitud
headers = {
    "Ocp-Apim-Subscription-Key": API_KEY,
    "Content-Type": "application/json"
}

# Cuerpo del JSON corregido
json_payload = {
    "projectFileVersion": "2022-10-01-preview",
    "stringIndexType": "Utf16CodeUnit",
    "metadata": {
        "projectKind": "Conversation",
        "settings": {
            "confidenceThreshold": 0.7
        },
        "projectName": "Dell Product Information",
        "multilingual": True,
        "description": "Analysis of Dell product specifications",
        "language": "es"
    },
    "assets": {
        "projectKind": "Conversation",
        "intents": [
            {
                "category": "ConsultarProducto"
            },
            {
                "category": "SolicitarPrecio"
            },
            {
                "category": "ConsultarGarantia"
            }
        ],
        "entities": [
            {
                "category": "Producto",
                "subentities": []
            },
            {
                "category": "Precio",
                "subentities": []
            },
            {
                "category": "Garantia",
                "subentities": []
            }
        ],
        "utterances": [
            {
                "text": "¿Qué características tiene el Dell XPS 14?",
                "dataset": "ProductInqueries",
                "intent": "ConsultarProducto",
                "entities": [
                    {
                        "category": "Producto",
                        "offset": 32,
                        "length": 11
                    }
                ]
            },
            {
                "text": "¿Cuál es el precio del Dell XPS 14?",
                "language": "es",
                "dataset": "PricingInquiries",
                "intent": "SolicitarPrecio",
                "entities": [
                    {
                        "category": "Producto",
                        "offset": 26,
                        "length": 11
                    },
                    {
                        "category": "Precio",
                        "offset": 36,
                        "length": 5
                    }
                ]
            },
            {
                "text": "¿Cuánto dura la garantía del Dell XPS 14?",
                "dataset": "WarrantyInquiries",
                "intent": "ConsultarGarantia",
                "entities": [
                    {
                        "category": "Producto",
                        "offset": 31,
                        "length": 11
                    },
                    {
                        "category": "Garantia",
                        "offset": 26,
                        "length": 7
                    }
                ]
            },
            {
                "text": "Dame detalles sobre la batería y carga del Dell XPS 14.",
                "language": "es",
                "dataset": "ProductInqueries",
                "intent": "ConsultarProducto",
                "entities": [
                    {
                        "category": "Producto",
                        "offset": 43,
                        "length": 11
                    }
                ]
            },
            {
                "text": "¿Puedes decirme el precio de la Dell XPS 14?",
                "dataset": "PricingInquiries",
                "intent": "SolicitarPrecio",
                "entities": [
                    {
                        "category": "Producto",
                        "offset": 30,
                        "length": 11
                    },
                    {
                        "category": "Precio",
                        "offset": 40,
                        "length": 5
                    }
                ]
            },
            {
                "text": "¿Cuál es la duración de la garantía del Dell XPS 14?",
                "language": "es",
                "dataset": "WarrantyInquiries",
                "intent": "ConsultarGarantia",
                "entities": [
                    {
                        "category": "Producto",
                        "offset": 38,
                        "length": 11
                    },
                    {
                        "category": "Garantia",
                        "offset": 29,
                        "length": 7
                    }
                ]
            }
        ]
    }
}
# Enviar la solicitud a Azure
response = requests.post(url, headers=headers, json=json_payload)

# Verificar si la solicitud fue aceptada
if response.status_code == 202:
    operation_url = response.headers.get("operation-location")
    if operation_url:
        print(f"✅ Importación iniciada. Monitoreando operación en: {operation_url}")

        # Consultar el estado de la operación cada 5 segundos hasta que termine
        while True:
            status_response = requests.get(operation_url, headers=headers)
            status_data = status_response.json()

            # Mostrar estado actual
            print(f"⏳ Estado actual: {status_data.get('status')}")

            if status_data.get("status") in ["succeeded", "failed"]:
                print(f"🚀 Operación completada. Estado final: {status_data.get('status')}")
                print("📌 Respuesta completa:", status_data)
                break

            time.sleep(5)  # Esperar antes de la siguiente consulta

    else:
        print("❌ No se encontró la URL de seguimiento en la respuesta.")
else:
    print(f"❌ Error en la solicitud. Código {response.status_code}")
    print("📌 Respuesta JSON:", response.text)