from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()
    Year = forms.CharField(required=True)
    Exp_Name = forms.CharField(required=True)
