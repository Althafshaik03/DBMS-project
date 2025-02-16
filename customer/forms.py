from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from . import models

class CustomerUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalpha():
            raise ValidationError("First name should contain only alphabets.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.isalpha():
            raise ValidationError("Last name should contain only alphabets.")
        return last_name

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')

        # Check if password exists (required field)
        if not password:
            self.add_error('password', "Password is required.")
            return cleaned_data  # Stop further validation if password is missing

        # Password strength validation
        if len(password) < 8:
            self.add_error('password', "Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            self.add_error('password', "Password must contain at least one digit.")
        if not any(char.isalpha() for char in password):
            self.add_error('password', "Password must contain at least one letter.")

class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ['address', 'mobile', 'profile_pic']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if not mobile.isdigit():
            raise ValidationError("Mobile number must contain only digits.")
        if len(mobile) != 10:
            raise ValidationError("Mobile number must be 10 digits long.")
        return mobile