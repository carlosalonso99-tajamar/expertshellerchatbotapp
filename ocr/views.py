from django.shortcuts import render, redirect, get_object_or_404
from .models import UploadedPDF
from .forms import UploadFilesForm
from projects.models import Project
from openai_processing.services import OpenAIService
from openai_processing.models import GeneratedJSON

def upload_documents(request, project_id):
    """
    Vista para subir múltiples documentos y vincularlos a un proyecto.
    """
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        form = UploadFilesForm(request.POST, request.FILES)

        if form.is_valid():
            files = request.FILES.getlist("files")  # Obtener lista de archivos subidos

            if files:
                documents = []
                for file in files:
                    doc = UploadedPDF.objects.create(file=file)
                    documents.append(doc)

                project.documents.add(*documents)

                # Generar JSON automáticamente con los documentos subidos
                json_result = OpenAIService.generate_structured_json(documents)

                # Guardar el JSON en la base de datos
                json_instance = GeneratedJSON()
                json_instance.save_json(json_result)
                project.json_file = json_instance
                project.save()

                return redirect("project_detail", project_id=project.id)

    else:
        form = UploadFilesForm()

    return render(request, "upload_documents.html", {"form": form, "project": project})
