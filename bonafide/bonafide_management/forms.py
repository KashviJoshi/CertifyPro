from django import forms
from .models import Student, CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "Name",
            "Fathers_Name",
            "Email",
            "Department_Choice",
            "Passing_Year",
            "Phone",
            "University_Roll_Number",
            "Write_Purpose",
        ]
