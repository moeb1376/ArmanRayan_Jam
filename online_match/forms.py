from django import forms
from .models import Code

class CodeUploadForm(forms.ModelForm):
    class Meta:
        model = Code
        fields = ['code']
