from django import forms

class LanguageForm(forms.Form):
    language = forms.CharField(label='Язык', max_length=100)
