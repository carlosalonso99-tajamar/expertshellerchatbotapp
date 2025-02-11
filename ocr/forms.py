from django import forms

class UploadFilesForm(forms.Form):
    files = forms.FileField(
        widget=forms.FileInput(attrs={"accept": "application/pdf"}), 
        required=True
    )
