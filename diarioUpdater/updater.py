from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from diarioUpdater import diarioUpdater

def start():
    diarioUpdater.update_diario()
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(diarioUpdater.update_diario, 'interval', seconds=10)
    # scheduler.start()