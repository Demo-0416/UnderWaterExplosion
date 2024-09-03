from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()
    year = forms.CharField(max_length=4, help_text='Enter year')
    exp_name = forms.CharField(help_text='Enter experiment name')
