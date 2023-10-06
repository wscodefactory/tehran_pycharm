from django import forms
from .models import User

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['id', 'password', 'email', 'name']
        widgets = {
            'password': forms.PasswordInput(),
        }

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['id', 'password']