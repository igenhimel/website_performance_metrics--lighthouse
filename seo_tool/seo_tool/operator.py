# operator.py

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from cronjob.views import cronjob
from cronjob.models import JobExecutionLog, ScheduledJob
from datetime import datetime
from pytz import timezone
from datetime import timedelta

scheduler = None

def initialize_scheduler():
    global scheduler
    if scheduler is None:
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
        register_events(scheduler)

def start(job_name):
    global scheduler

    if scheduler is None:
        initialize_scheduler()

    # Check if the job is already scheduled, if so, return
    if scheduler.get_job(job_name):
        return

    cron_job_interval = ScheduledJob.objects.get(job_name=job_name)

    if cron_job_interval:
        interval_minutes = cron_job_interval.time_minutes
    else:
        interval_minutes = 10  # Default value if no interval is found

    def page_speed():
        cron_job_interval = ScheduledJob.objects.get(job_name=job_name)

        if cron_job_interval:
            interval_minutes = cron_job_interval.time_minutes
        else:
            interval_minutes = 10

        start_message = f"Job '{job_name}' started."

        job_execution_log = JobExecutionLog(
            job_name=job_name,
            start_message=start_message,
            start_time=datetime.now(timezone('Asia/Dhaka')),
            finish_time=None,
        )
        job_execution_log.save()

        cronjob()

        job_execution_log.finish_time = datetime.now(timezone('Asia/Dhaka'))
        job_execution_log.save()

        scheduler.reschedule_job(
            job_name,
            trigger='interval',
            minutes=interval_minutes,
            next_run_time=datetime.now(timezone('Asia/Dhaka')) + timedelta(minutes=interval_minutes)
        )

    scheduler.add_job(
        page_speed,
        'interval',
        minutes=interval_minutes,
        id=job_name,
        next_run_time=datetime.now(timezone('Asia/Dhaka')) + timedelta(minutes=interval_minutes)
    )

    if not scheduler.running:
        scheduler.start()

def pause(job_name):
    global scheduler

    if scheduler is None:
        initialize_scheduler()

    if scheduler.get_job(job_name):
        scheduler.pause_job(job_name)

def resume(job_name):
    global scheduler

    if scheduler is None:
        initialize_scheduler()

    if scheduler.get_job(job_name):
        scheduler.resume_job(job_name)
