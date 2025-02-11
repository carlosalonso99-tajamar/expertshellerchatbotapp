from django.contrib import admin

# Register your models here.

#Register the models
from .models import Project
admin.site.register(Project)