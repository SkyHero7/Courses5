from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from new_users.models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'phone', 'city', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_active', 'city')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('phone', 'city', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'city', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'phone', 'city')
    ordering = ('email',)

if not admin.site.is_registered(CustomUser):
    admin.site.register(CustomUser, CustomUserAdmin)
