from django.contrib import admin
from django.contrib.auth.models import Group, Permission

from new_users.models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_verified')

    def is_verified(self, obj):
        return obj.is_verified
    is_verified.boolean = True

admin.site.register(CustomUser, CustomUserAdmin)

manager_group, created = Group.objects.get_or_create(name='Managers')
if created:
    permissions = Permission.objects.filter(content_type__app_label='your_app_label')
    manager_group.permissions.set(permissions)
