from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()


class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=User.Role.choices,
        initial=User.Role.STUDENT,
        widget=forms.RadioSelect(attrs={"class": "inline-flex gap-4"}),
    )

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "role", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Username", "class": "form-input"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email", "class": "form-input"}),
            "first_name": forms.TextInput(attrs={"placeholder": "First name", "class": "form-input"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name", "class": "form-input"}),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Username", "class": "form-input", "autofocus": True}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "form-input"}),
    )
