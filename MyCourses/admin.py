from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from .models import Mailing, CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_verified')

# Регистрация модели CustomUser
admin.site.register(CustomUser, CustomUserAdmin)

# Создание группы менеджеров и определение их прав доступа
manager_group, created = Group.objects.get_or_create(name='Managers')
if created:
    # Назначение прав доступа
    permissions = Permission.objects.filter(content_type__app_label='your_app_label')
    manager_group.permissions.set(permissions)

