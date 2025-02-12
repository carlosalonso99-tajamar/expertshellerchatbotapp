"""
This code sample shows Prebuilt Layout operations with the Azure AI Document Intelligence client library.
The async versions of the samples require Python 3.8 or later.

To learn more, please visit the documentation - Quickstart: Document Intelligence (formerly Form Recognizer) SDKs
https://learn.microsoft.com/azure/ai-services/document-intelligence/quickstarts/get-started-sdks-rest-api?pivots=programming-language-python
"""

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

"""
Remember to remove the key from your code when you're done, and never post it publicly. For production, use
secure methods to store and access your credentials. For more information, see 
https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-security?tabs=command-line%2Ccsharp#environment-variables-and-application-configuration
"""
endpoint = "https://doc-intel-carlos.cognitiveservices.azure.com/"
key = "4efSk8gz2TZLNqaaLI9Knhwta2Js1DoolPGsyeqIlQJI2agdhvDXJQQJ99BBACYeBjFXJ3w3AAALACOGjMSn"

# 🔹 Crear el cliente de Azure Document Intelligence
document_intelligence_client = DocumentIntelligenceClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

# 🔹 Ruta del archivo local
pdf_path = "./fichas-tecnicas/16Z90R-E.AD78B.pdf"

# 🔹 Leer el archivo en modo binario y enviarlo correctamente
with open(pdf_path, "rb") as pdf_file:
    poller = document_intelligence_client.begin_analyze_document(
        model_id="prebuilt-layout",  # Modelo preentrenado para texto/tablas
        document=pdf_file,  # Enviamos el archivo binario directamente
    )

# 🔹 Obtener los resultados del análisis
result = poller.result()

# 🔹 Imprimir el contenido extraído
for page in result.pages:
    print(f"📄 Página {page.page_number}")
    for line in page.lines:
        print(line.content)

for table_idx, table in enumerate(result.tables):
    print(f"📊 Tabla {table_idx} - Filas: {table.row_count}, Columnas: {table.column_count}")
    for cell in table.cells:
        print(f"Celda[{cell.row_index}][{cell.column_index}]: {cell.content}")

print("✅ ¡Extracción completada con éxito!")