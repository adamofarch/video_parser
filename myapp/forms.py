from django import forms
from .models import Vid


class Vid_Form(forms.ModelForm):
    vid_name = forms.CharField(
        label='Title',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Title'
        })
    )

    vid_file = forms.FileField(
        allow_empty_file=False,
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Vid
        fields = ['vid_name', 'vid_file']

class search_query_form(forms.Form):
    search_query = forms.CharField(
        label = '',
        required = False,
        widget=forms.TextInput(attrs={
            'class': 'form-control me-2',
            'type': 'search',
            'placeholder': 'Search', 
            'aria-label': 'Search'
        })
    )
