from django import forms
from django.core.validators import EmailValidator, MinLengthValidator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput
from .models import UserProfile
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator


# - Create/Register a user (Model Form)
class CreateUserForm(UserCreationForm):
    email = forms.EmailField(
        validators=[EmailValidator(message="Invalid email address.")]
    )
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)

    class meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


# Authenticate a user (Model form)
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(), required=True)
    password = forms.CharField(widget=PasswordInput(), required=True)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["bio", "profile_picture"]
