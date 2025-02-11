from django import forms

class DocumentContextForm(forms.Form):
    intent = forms.CharField(label="Intención del documento", max_length=255)
    entities = forms.CharField(label="Entidades clave (separadas por comas)", widget=forms.Textarea)
