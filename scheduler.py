import sched
import time
from datetime import datetime, timedelta

import os
import django
from django.core.mail import send_mail
from django.conf import settings
from MyCourses.models import Mailing, Message, SendingAttempt, MailingSrv

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
django.setup()

def send_mailing():
    current_datetime = datetime.now()
    mailings = MailingSrv.objects.filter(next__lte=current_datetime, status='создана')

    for mailing in mailings:
        message = mailing.mail
        clients = mailing.recipients.all()

        for client in clients:
            try:
                send_mail(
                    subject=message.subject,
                    message=message.body,
                    from_email='your_email@example.com',
                    recipient_list=[client.email],
                    fail_silently=False,
                )
                SendingAttempt.objects.create(mailing=mailing, client=client, status='success')
            except Exception as e:
                SendingAttempt.objects.create(mailing=mailing, client=client, status='failure', server_response=str(e))

        mailing.next = calculate_next_send_datetime(mailing)
        mailing.save()

def calculate_next_send_datetime(mailing):
    if mailing.frequency == MailingSrv.AT_ONCE:
        return None
    elif mailing.frequency == MailingSrv.BY_DAY:
        return mailing.next + timedelta(days=1)
    elif mailing.frequency == MailingSrv.BY_WEEK:
        return mailing.next + timedelta(weeks=1)
    elif mailing.frequency == MailingSrv.BY_MONTH:
        return mailing.next + timedelta(days=30)
    return None

if __name__ == '__main__':
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(0, 1, send_mailing, (scheduler,))
    scheduler.run()
