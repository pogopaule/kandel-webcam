from webcam import run
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=15)
def timed_job():
    run()

sched.start()
