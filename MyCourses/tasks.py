from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.core.management import call_command

# Создание объекта планировщика задач
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

# Регистрация задачи отправки рассылок
scheduler.add_job(call_command, "interval", minutes=5, args=["run_mailings"], id="send_mailings")

# Запуск планировщика задач
scheduler.start()
