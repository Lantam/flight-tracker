from django import forms
from map.models import Search


class SearchForm(forms.ModelForm):
    location = forms.CharField(label='')

    class Meta:
        model = Search
        fields = ['location',]
