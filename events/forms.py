from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_name', 'date', 'phone_number', 'location', 'description', 'capacity']
        widgets = {
            'date': forms.DateInput(
                format='%d-%m-%Y',  
                attrs={
                    'placeholder': 'dd/mm/yyyy',
                    'class': 'form-control',
                    'type': 'date',  
                }
            ),
        }


