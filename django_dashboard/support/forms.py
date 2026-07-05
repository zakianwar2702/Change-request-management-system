from django import forms
from .models import SupportTicket


class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['title', 'requester', 'status', 'priority', 'project', 'attachment']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter the title for the request'}),
            'requester': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter requester name'}),
            'status': forms.Select(attrs={'class': 'input-field'}),
            'priority': forms.Select(attrs={'class': 'input-field'}),
            'project': forms.Select(attrs={'class': 'input-field'}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'input-field'}),
        }
