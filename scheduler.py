from apscheduler.schedulers.blocking import BlockingScheduler
from mailing_script import send_mailing

scheduler = BlockingScheduler()

scheduler.add_job(send_mailing, 'interval', minutes=30)

scheduler.start()