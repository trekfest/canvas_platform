from django import forms
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserAdmin(UserAdmin):
    form = CustomUserForm    