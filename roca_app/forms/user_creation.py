from django import forms
from django.contrib.auth.models import User

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,label='Contraseña')
    confirm_password = forms.CharField(widget=forms.PasswordInput,label='Confirmar Contraseña')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'password']
        labels = {
            'username': 'Usuario',
            'first_name': 'Nombre',
        }
        help_texts = {
            'username': '',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
