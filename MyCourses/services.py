from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from MyCourses.models import Mailing, Message, SendingAttempt, MailingSrv


def send_mailing():
    current_datetime = timezone.now()

    # Получение рассылок, которые должны быть отправлены
    mailings = MailingSrv.objects.filter(next__lte=current_datetime, status=MailingSrv.CREATED, is_activated=True)

    for mailing in mailings:
        message = mailing.mail
        recipients = mailing.recipients.all()

        for recipient in recipients:
            try:
                send_mail(
                    subject=message.subject,
                    message=message.body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient.email],
                    fail_silently=False,
                )
                SendingAttempt.objects.create(mailing=mailing, client=recipient, status='success')
            except Exception as e:
                SendingAttempt.objects.create(mailing=mailing, client=recipient, status='failure', server_response=str(e))

        # Обновление времени следующей рассылки в зависимости от частоты
        if mailing.frequency == MailingSrv.AT_ONCE:
            mailing.status = MailingSrv.FINISHED
        elif mailing.frequency == MailingSrv.BY_DAY:
            mailing.next = current_datetime + timedelta(days=1)
        elif mailing.frequency == MailingSrv.BY_WEEK:
            mailing.next = current_datetime + timedelta(weeks=1)
        elif mailing.frequency == MailingSrv.BY_MONTH:
            mailing.next = current_datetime + timedelta(weeks=4)

        mailing.save()