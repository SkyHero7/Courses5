from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.conf import settings

class Command(BaseCommand):
    help = 'Runs the mailings'

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Регистрация задачи отправки рассылок
        scheduler.add_job(call_command, "interval", minutes=5, args=["run_mailings"], id="send_mailings")

        # Запуск планировщика задач
        scheduler.start()

        try:
            # Бесконечный цикл, чтобы процесс не завершился
            while True:
                pass
        except KeyboardInterrupt:
            # Остановка планировщика задач при нажатии Ctrl+C
            scheduler.shutdown()