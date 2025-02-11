from django.shortcuts import render, redirect
from .forms import DocumentContextForm
from ocr.models import UploadedPDF

def document_context(request):
    """
    Vista que solicita al usuario que defina intenciones y entidades después de la carga de PDFs.
    """
    if request.method == "POST":
        form = DocumentContextForm(request.POST)
        if form.is_valid():
            request.session["intent"] = form.cleaned_data["intent"]
            request.session["entities"] = form.cleaned_data["entities"]
            
            # Redirigir a la generación del JSON con OpenAI
            return redirect("process_texts")  

    else:
        form = DocumentContextForm()

    return render(request, "document_context.html", {"form": form})


from django.shortcuts import render
from .models import GeneratedJSON
from .services import OpenAIService

def process_texts(request):
    """
    Toma los textos extraídos de los PDFs, las intenciones y entidades del usuario,
    y los envía a OpenAI para generar un JSON estructurado.
    """
    intent = request.session.get("intent", "")
    entities = request.session.get("entities", "").split(",")
    documents = UploadedPDF.objects.all()

    if not documents.exists():
        return render(request, "openai_processing/json_result.html", {"json_result": "No hay documentos procesados."})

    # Generar JSON con OpenAI y guardarlo
    json_result = OpenAIService.generate_structured_json(intent, entities, documents)

    return render(request, "openai_processing/json_result.html", {"json_result": json_result})

def list_json_files(request):
    """
    Lista todos los JSON generados para su visualización y descarga.
    """
    json_files = GeneratedJSON.objects.all()
    return render(request, "list_json.html", {"json_files": json_files})
