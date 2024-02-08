from django import forms
from django.contrib.auth.forms import UserCreationForm
from tracker.models import User, Book


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class NewBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "cover", "page_count", "series"]
