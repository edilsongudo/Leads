from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import schedule_db_backup


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_db_backup, 'interval', minutes=10)
    scheduler.start()
