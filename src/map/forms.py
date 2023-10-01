from django import forms
from .models import Search


class SearchForm(forms.ModelForm):
    location = forms.CharField(label='')

    class Meta:
        model = Search
        fields = ['location',]
