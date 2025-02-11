from django.shortcuts import render, redirect, get_object_or_404
from .models import Project
from .forms import ProjectForm


def create_project(request):
    """
    Vista para crear un nuevo proyecto.
    """
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            return redirect("projects:list")  # Redirigir a la lista de proyectos
    else:
        form = ProjectForm()
    
    return render(request, "create_project.html", {"form": form})


def project_detail(request, project_id):
    """
    Vista para mostrar los detalles de un proyecto.
    """
    project = get_object_or_404(Project, id=project_id)
    return render(request, "project_detail.html", {"project": project})



def list_projects(request):
    """
    Vista para listar todos los proyectos creados.
    """
    projects = Project.objects.all()
    return render(request, "list_projects.html", {"projects": projects})


def project_detail(request, project_id):
    """
    Vista para mostrar los detalles de un proyecto.
    """
    project = get_object_or_404(Project, id=project_id)
    return render(request, "project_detail.html", {"project": project})
