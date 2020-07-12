from django import forms
from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'username','first_name','last_name','password','image','date_joined','update_on','about')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_trustee','is_authority','is_admin')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','username','first_name','last_name', 'is_staff', 'is_active','is_trustee','is_authority')}
        ),
    )
    search_fields = ('email','username')
    ordering = ('email','username')
    readonly_fields=['date_joined','update_on']

admin.site.register(CustomUser, CustomUserAdmin)

#this is for file models
from .models import Files
admin.site.register(Files)