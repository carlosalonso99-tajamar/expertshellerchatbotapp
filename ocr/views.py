from django.shortcuts import render, redirect, get_object_or_404
from .models import UploadedPDF
from .forms import UploadFilesForm
from projects.models import Project
from openai_processing.models import GeneratedJSON
from openai_processing.services import OpenAIService
from ocr.services import OCRService  # Importamos el servicio OCR
import os, json

#TODO: mecanismo para evitar duplicidad de pdfs 
def upload_documents(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    ocr_service = OCRService()  # Instancia del servicio OCR

    if request.method == "POST":
        form = UploadFilesForm(request.POST, request.FILES)

        if form.is_valid():
            files = request.FILES.getlist("files")

            if files:
                documents = []
                for file in files:
                    # Guardamos el archivo PDF en la base de datos
                    doc = UploadedPDF.objects.create(file=file)
                    
                    # Procesamos el PDF con OCR para extraer texto
                    pdf_path = doc.file.path  # Ruta del archivo guardado
                    extracted_text = ocr_service.extract_text_from_pdf(pdf_path)

                    if extracted_text:
                        doc.extracted_text = extracted_text  # Guardamos el texto en el modelo
                        doc.save()

                    documents.append(doc)

                project.documents.add(*documents)

                # Generar JSON automáticamente después del OCR
                json_result = OpenAIService.generate_structured_json(documents)

                if json_result:
                    json_instance = GeneratedJSON.objects.create()
                    
                    # Guardamos el JSON como archivo
                    json_filename = f"{json_instance.id}.json"
                    json_path = os.path.join("media", "json-outputs", json_filename)

                    with open(json_path, "w", encoding="utf-8") as json_file:
                        json.dump(json_result, json_file, indent=4, ensure_ascii=False)

                    # Asociamos el archivo al objeto
                    json_instance.file.name = f"json-outputs/{json_filename}"
                    json_instance.save()

                    # Asociamos el JSON al proyecto
                    project.json_file = json_instance
                    project.save()
                
                return redirect("projects:project_detail", project_id=project.id)

    else:
        form = UploadFilesForm()

    return render(request, "upload_documents.html", {"form": form, "project": project})
