from django.urls import path
from .views import create_project, list_projects, project_detail#, create_chatbot

app_name = "projects"  # IMPORTANTE para que el `url 'projects:list'` funcione

urlpatterns = [
    path("", list_projects, name="list"),
    path("create/", create_project, name="create"),
    path("<uuid:project_id>/", project_detail, name="project_detail"),
    # path("<uuid:project_id>/create-chatbot/", create_chatbot, name="create_chatbot"),
]
