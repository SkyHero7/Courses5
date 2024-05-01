from django.db import models
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
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
        ('monthly', 'Раз в месяц')
    ]

    send_datetime = models.DateTimeField()
    frequency = models.CharField(max_length=20, choices=SEND_CHOICES)
    status = models.CharField(max_length=20)
    message = models.ForeignKey('Message', on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client, related_name='mailings')

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

class SendingAttempt(models.Model):
    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failure', 'Не успешно')
    ]

    send_datetime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    server_response = models.TextField()
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.status} - {self.send_datetime}"

    def save(self, *args, **kwargs):
        try:
            self.server_response = send_mail(
                self.mailing.message.subject,
                self.mailing.message.body,
                settings.EMAIL_HOST_USER,
                [client.email for client in self.mailing.clients.all()],
                fail_silently=False
            )
            self.status = 'success'
        except smtplib.SMTPException as e:
            self.server_response = str(e)
            self.status = 'failure'
        super().save(*args, **kwargs)

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
