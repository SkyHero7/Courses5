from django.db import models
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from django.utils import timezone
import smtplib

class Client(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    email = models.EmailField()
    full_name = models.CharField(max_length=100)
    comment = models.TextField()

    def __str__(self):
        return self.full_name

class Mailing(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    SEND_CHOICES = [
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    ]

    send_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    next_send_datetime = models.DateTimeField()
    frequency = models.CharField(max_length=20, choices=SEND_CHOICES)
    status = models.CharField(max_length=20)
    message = models.ForeignKey('Message', on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client, related_name='mailings')
    end_datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.message.subject} - {self.send_datetime}"

    def clean(self):
        if self.send_datetime < timezone.now():
            raise ValidationError("Дата и время отправки должны быть в будущем")

class Message(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    subject = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return self.subject


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

class MailingSrv(models.Model):
    """
    Модель для хранения информации о рассылках.
    """

    AT_ONCE = 'один раз'
    BY_DAY = 'раз в день'
    BY_WEEK = 'раз в неделю'
    BY_MONTH = 'раз в месяц'

    FREQUENCY = [
        (AT_ONCE, 'один раз'),
        (BY_DAY, 'раз в день'),
        (BY_WEEK, 'раз в неделю'),
        (BY_MONTH, 'раз в месяц')
    ]

    CREATED = 'создана'
    PROCESSING = 'запущена'
    FINISHED = 'завершена'

    STATUS = [
        (CREATED, 'создана'),
        (PROCESSING, 'запущена'),
        (FINISHED, 'завершена')
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь', null=True, blank=True)
    recipients = models.ManyToManyField(Client, verbose_name='получатели рассылки')
    start = models.DateTimeField(default=timezone.now, verbose_name='время начала рассылки')
    next = models.DateTimeField(default=timezone.now, verbose_name='время следующей рассылки')
    finish = models.DateTimeField(verbose_name='время завершения рассылки')
    status = models.CharField(max_length=100, choices=STATUS, default=CREATED, verbose_name='статус рассылки')
    frequency = models.CharField(max_length=50, choices=FREQUENCY, verbose_name='периодичность рассылки')
    is_activated = models.BooleanField(default=True, verbose_name='метка активности')

    def __str__(self):
        return f'Рассылка_{self.pk}: {self.frequency} - {self.status}'

class SendingAttempt(models.Model):
    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failure', 'Не успешно')
    ]
    mailing = models.ForeignKey(MailingSrv, on_delete=models.CASCADE, verbose_name='рассылка')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='клиент')
    status = models.CharField(max_length=100, verbose_name='статус')
    server_response = models.TextField(blank=True, null=True, verbose_name='ответ сервера')
    timestamp = models.DateTimeField(default=timezone.now, verbose_name='время отправки')

    def __str__(self):
        return f"{self.status} - {self.send_datetime}"
