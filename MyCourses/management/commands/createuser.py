from django.core.management.base import BaseCommand
from users.models import CustomUser

class Command(BaseCommand):
    help = 'Создает нового пользователя'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Адрес электронной почты пользователя')
        parser.add_argument('password', type=str, help='Пароль пользователя')

    def handle(self, *args, **kwargs):
        email = kwargs['email']
        password = kwargs['password']
        user = CustomUser.objects.create_user(email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'Пользователь успешно создан с email: {email}'))

