from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from projects.models import Project

def home(request):
    projects = Project.objects.all()  # O usa un filtro según usuario si hay autenticación
    return render(request, "home.html", {"projects": projects})


def convert_pdf_to_text(request):
    return render(request, "convert_pdf_to_text.html")