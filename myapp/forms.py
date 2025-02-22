from django import forms
from .models import Vid


class Vid_Form(forms.ModelForm):
    vid_url = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-5 py-3 rounded-xl bg-white dark:bg-gray-900/50 border-2 border-gray-200 dark:border-gray-700 focus:outline-none focus:border-purple-500 dark:focus:border-cyan-400 focus:ring-2 focus:ring-purple-500/30 dark:focus:ring-cyan-400/30 transition-all duration-300',
            'placeholder': 'Paste video URL here...',
            'id': 'videoURL'
        })
    )

    vid_file = forms.FileField(
        allow_empty_file=False,
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'hidden',
            'id': 'fileInput',
            'accept': 'video/*'

        })
    )

    class Meta:
        model = Vid
        fields = ['vid_url', 'vid_file']

class search_query_form(forms.Form):
    search_query = forms.CharField(
        label = '',
        required = False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 rounded-xl bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-purple-500/50 dark:focus:ring-cyan-400/50 transition-all duration-300 shadow-sm',
            'type': 'text',
            'placeholder': 'Search subs...', 
        })
    )
