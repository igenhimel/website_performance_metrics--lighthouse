# operator.py

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from seo_checker.views import seo_checker
from seo_checker.models import JobExecutionLog  # Import your model
from datetime import datetime  # Import datetime for updating finish_time

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)

    # Check if the job with the name 'page_speed' exists
    existing_jobs = scheduler.get_jobs()
    job_exists = any(job.name == 'page_speed' for job in existing_jobs)

    if job_exists:
        # Remove the existing 'page_speed' job
        for job in existing_jobs:
            if job.name == 'page_speed':
                scheduler.remove_job(job.id)

    @scheduler.scheduled_job('interval', minutes=10, name='page_speed')
    def auto_hello():
        # Log the start message
        start_message = "Job 'page_speed' started."
        
        # Record job execution in the database with start_time
        job_execution_log = JobExecutionLog(
            job_name='page_speed',
            start_message=start_message,
        )
        job_execution_log.save()

        # Execute the SEO checker
        seo_checker()

        # Update finish_time when the job finishes
        job_execution_log.finish_time = datetime.now()
        job_execution_log.save()

    scheduler.start()
