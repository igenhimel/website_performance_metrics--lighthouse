# operator.py

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from cronjob.views import cronjob
from cronjob.models import JobExecutionLog, ScheduledJob  # Import your model
from datetime import datetime  # Import datetime for updating finish_time
from pytz import timezone
from datetime import timedelta


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)

    cron_job_interval = ScheduledJob.objects.first()

    if cron_job_interval:
        interval_minutes = cron_job_interval.time_minutes
    else:
        interval_minutes = 10  # Default value if no interval is found

    def page_speed():
        # Retrieve the interval value from the database
        cron_job_interval = ScheduledJob.objects.first()

        if cron_job_interval:
            interval_minutes = cron_job_interval.time_minutes
        else:
            interval_minutes = 10  # Default value if no interval is found

        # Log the start message
        start_message = "Job 'page_speed' started."

        # Record job execution in the database with start_time
        job_execution_log = JobExecutionLog(
            job_name='page_speed',
            start_message=start_message,
            start_time=datetime.now(timezone('Asia/Dhaka')),
            finish_time=None,
        )
        job_execution_log.save()

        # Execute the cron
        cronjob()

        # Update finish_time when the job finishes
        job_execution_log.finish_time = datetime.now(timezone('Asia/Dhaka'))
        job_execution_log.save()

        # Set the next job interval dynamically
        scheduler.reschedule_job(
            'page_speed',
            trigger='interval',
            minutes=interval_minutes,
            next_run_time=datetime.now(timezone('Asia/Dhaka')) + timedelta(minutes=interval_minutes)
        )

    scheduler.add_job(
        page_speed,
        'interval',
        minutes=interval_minutes,
        id='page_speed',
        next_run_time=datetime.now(timezone('Asia/Dhaka')) + timedelta(minutes=interval_minutes)
    )

    scheduler.start()
