from django.urls import path
from .views import create_clu_project

app_name = "clu"

urlpatterns = [
    path("create/<uuid:project_id>/", create_clu_project, name="create_clu_project"),
]
