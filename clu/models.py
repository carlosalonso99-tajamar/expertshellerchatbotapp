from django.db import models
from projects.models import Project


    
from django.db import models
from projects.models import Project

class CLUProject(models.Model):
    project = models.OneToOneField(
        Project, on_delete=models.CASCADE, related_name="clu_project"
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    azure_project_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=[("CREATED", "Created"), ("TRAINED", "Trained"), ("DEPLOYED", "Deployed")],
        default="CREATED"
    )

    def __str__(self):
        return self.name
