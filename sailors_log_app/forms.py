from django import forms

from sailors_log_app.models import Trip


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['title', 'boat', 'description', 'gpx_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input'}),
            'boat': forms.Select(attrs={'class': 'select'}),
            'description': forms.Textarea(attrs={'class': 'textarea'}),
            'gpx_file': forms.ClearableFileInput(attrs={'class': 'file-input'}),
        }
