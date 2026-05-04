from django import forms
from .models import Service


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['category', 'name', 'description', 'duration', 'price', 'is_active', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }
