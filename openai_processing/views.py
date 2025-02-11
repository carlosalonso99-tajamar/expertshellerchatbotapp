from django.shortcuts import render

from django.shortcuts import render
from .models import GeneratedJSON

def list_json_files(request):
    """
    Lista todos los JSON generados para su visualización y descarga.
    """
    json_files = GeneratedJSON.objects.all()
    return render(request, "list_json.html", {"json_files": json_files})

