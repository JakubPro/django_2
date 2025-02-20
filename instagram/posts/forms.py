from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Nazwa użytkownika: ",
        widget=forms.TextInput(attrs={'placeholder': 'Twoja nazwa użytkownika'}),
    )
    
    password1 = forms.CharField(
        label="Hasło: ",
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Wprowadź hasło'}),
    )
    password2 = forms.CharField(
        label="Potwierdzenie hasła: ",
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Potwierdź hasło'}),
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    
