from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'method', 'discount', 'notes']
        widgets = {
            'amount':   forms.NumberInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes':    forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }
