from django import forms
from .models import Master


class MasterForm(forms.ModelForm):
    class Meta:
        model = Master
        fields = ['display_name', 'phone', 'bio', 'photo', 'color', 'is_active', 'calendar_order', 'specializations']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'color': forms.TextInput(attrs={'type': 'color'}),
            'specializations': forms.CheckboxSelectMultiple(),
        }
