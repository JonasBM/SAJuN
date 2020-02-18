from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from diarioUpdater import diarioUpdater

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(diarioUpdater.update_diario, 'interval', minutes=1)
    scheduler.start()