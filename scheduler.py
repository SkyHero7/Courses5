import sched

from django.core.mail import send_mail
from datetime import datetime, timedelta, time
from MyCourses.models import Mailing, Message, SendingAttempt


def send_mailing(sc):
    current_datetime = datetime.now()

    mailings = Mailing.objects.filter(send_datetime__lte=current_datetime, status='created')

    for mailing in mailings:
        message = Message.objects.get(mailing=mailing)
        clients = mailing.clients.all()

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

    sc.enter(60, 1, send_mailing, (sc,))


if __name__ == '__main__':
    send_mailing()
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(0, 1, send_mailing, (scheduler,))
    scheduler.run()