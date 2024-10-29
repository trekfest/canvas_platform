from django.contrib import admin
from .models import CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('email', 'username', 'first_name', 'last_name')
