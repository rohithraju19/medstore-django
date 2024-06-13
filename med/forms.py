from django import forms
from .models import Customer
class LoginModelForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['email', 'password']