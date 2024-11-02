from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserForm

class CustomUserAdmin(UserAdmin):
    form = CustomUserForm
    list_display = ('id', 'email', 'username', 'first_name', 'last_name', 'role', 'is_active', 'is_staff')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('role', 'is_staff', 'is_active')

    # Make sure role field is included and editable in the fieldsets
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),  # Add the role field
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),  # Add the role field for adding new users
    )

    # Ensure you set this to True to allow editing
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj:  # If we are editing an existing user
            
            return fieldsets
        return fieldsets
    
    def get_readonly_fields(self, request, obj=None):
        # Make date_joined read-only
        return super().get_readonly_fields(request, obj) + ('date_joined','last_login')
    
admin.site.register(CustomUser, CustomUserAdmin)