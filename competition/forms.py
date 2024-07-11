from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Solution

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ['file']
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file.name.endswith('.py'):
            raise forms.ValidationError("Only .py files are allowed.")
        return file
