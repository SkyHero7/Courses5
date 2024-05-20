import sched
import time
from datetime import datetime

import os
import django
from django.core.mail import send_mail
from django.conf import settings
from MyCourses.models import Mailing, Message, SendingAttempt

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
django.setup()

def send_mailing(sc):
    current_datetime = datetime.now()

    mailings = Mailing.objects.filter(send_datetime__lte=current_datetime, status='created')

    for mailing in mailings:
        message = mailing.message
        clients = mailing.clients.all()

        for client in clients:
            try:
                send_mail(
                    subject=message.subject,
                    message=message.body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[client.email],
                    fail_silently=False,
                )
                SendingAttempt.objects.create(mailing=mailing, client=client, status='success')
            except Exception as e:
                SendingAttempt.objects.create(mailing=mailing, client=client, status='failure', server_response=str(e))

    sc.enter(60, 1, send_mailing, (sc,))

if __name__ == '__main__':
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(0, 1, send_mailing, (scheduler,))
    scheduler.run()
