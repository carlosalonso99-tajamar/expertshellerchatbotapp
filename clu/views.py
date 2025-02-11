import time
import requests
from django.shortcuts import render, redirect, get_object_or_404
from projects.models import Project
from clu.models import CLUProject
from clu.forms import CLUProjectForm
from clu.services import CLUService  # Servicio que maneja la API de Azure CLU

def create_clu_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Verificar si el proyecto tiene un JSON asociado
    if not project.json_file:
        return render(request, "create_clu_project.html", {
            "form": CLUProjectForm(),
            "project": project,
            "error": "No hay JSON generado para este proyecto. Debes procesar los documentos antes."
        })

    json_data = project.json_file.get_json()  # Obtener el JSON desde el archivo
    if not json_data:
        return render(request, "create_clu_project.html", {
            "form": CLUProjectForm(),
            "project": project,
            "error": "El JSON asociado está vacío o es inválido."
        })

    if request.method == "POST":
        form = CLUProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]

            # Llamar a Azure para crear el proyecto en CLU
            operation_url = CLUService.create_clu_project(name, description, json_data)

            if not operation_url:
                return render(request, "create_clu_project.html", {
                    "form": form,
                    "project": project,
                    "error": "No se pudo iniciar la importación en Azure CLU."
                })

            print(f"📡 Monitoreando importación en: {operation_url}")

            # 🔄 Esperar a que la importación finalice antes de continuar
            headers = {
                "Ocp-Apim-Subscription-Key": "TU_API_KEY_AQUI"
            }

            while True:
                response = requests.get(operation_url, headers=headers)

                if response.status_code == 200:
                    operation_status = response.json()
                    print(f"📡 Estado de importación: {operation_status}")

                    if operation_status.get("status") == "succeeded":
                        print("✅ Importación completada con éxito.")
                        break
                    elif operation_status.get("status") == "failed":
                        print("❌ Error: La importación falló.")
                        return render(request, "create_clu_project.html", {
                            "form": form,
                            "project": project,
                            "error": "La importación falló en Azure CLU."
                        })
                    else:
                        print("⏳ Aún en proceso, esperando 5 segundos...")
                else:
                    print(f"❌ Error al consultar el estado de la importación: {response.status_code}")
                    return render(request, "create_clu_project.html", {
                        "form": form,
                        "project": project,
                        "error": "No se pudo obtener el estado de la importación en Azure CLU."
                    })

                time.sleep(5)  # Esperar 5 segundos antes de volver a comprobar

            # Guardar el CLU Project una vez completado
            clu_project = CLUProject.objects.create(
                project=project,
                name=name,
                description=description,
                azure_project_id=name,  # El nombre en Azure es único
            )

            return redirect("projects:project_detail", project_id=project.id)

    else:
        form = CLUProjectForm()

    return render(request, "create_clu_project.html", {"form": form, "project": project})
