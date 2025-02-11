from django import forms
from .models import CLUProject

class CLUProjectForm(forms.ModelForm):
    class Meta:
        model = CLUProject
        fields = ["name", "description"]
