from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import redirect
from django.urls import path
from .models import ScheduledJob, JobExecutionLog
from django.urls import reverse
from seo_tool.operator import start, pause, resume

# Create a global dictionary to track job statuses
job_status_dict = {}

@admin.register(ScheduledJob)
class ScheduledJobAdmin(admin.ModelAdmin):
    list_display = ('job_name', 'time_minutes', 'is_running', 'start_button', 'pause_button', 'resume_button')

    def is_running(self, obj):
        return job_status_dict.get(obj.job_name, False)

    is_running.boolean = True
    is_running.short_description = 'Status'

    def start_selected_jobs(self, request, queryset):
        started_jobs = 0
        for job in queryset:
            if not job_status_dict.get(job.job_name, False):
                start(job.job_name)
                job_status_dict[job.job_name] = True
                started_jobs += 1
        if started_jobs > 0:
            self.message_user(request, f'Started {started_jobs} jobs successfully.')

    start_selected_jobs.short_description = 'Start Selected Jobs'

    def pause_selected_jobs(self, request, queryset):
        paused_jobs = 0
        for job in queryset:
            if job_status_dict.get(job.job_name, False):
                pause(job.job_name)
                job_status_dict[job.job_name] = False
                paused_jobs += 1
        if paused_jobs > 0:
            self.message_user(request, f'Paused {paused_jobs} jobs successfully.')

    pause_selected_jobs.short_description = 'Pause Selected Jobs'

    def resume_selected_jobs(self, request, queryset):
        resumed_jobs = 0
        for job in queryset:
            if not job_status_dict.get(job.job_name, False):
                resume(job.job_name)
                job_status_dict[job.job_name] = True
                resumed_jobs += 1
        if resumed_jobs > 0:
            self.message_user(request, f'Resumed {resumed_jobs} jobs successfully.')

    resume_selected_jobs.short_description = 'Resume Selected Jobs'

    # Custom buttons to trigger actions

    def start_button(self, obj):
        if not job_status_dict.get(obj.job_name, False):
            return format_html(
                '<a class="button" href="{}">Start</a>',
                reverse('admin:start_job', args=[obj.id])
            )
        return ''

    start_button.short_description = 'Start'

    def pause_button(self, obj):
        if job_status_dict.get(obj.job_name, False):
            return format_html(
                '<a class="button" href="{}">Pause</a>',
                reverse('admin:pause_job', args=[obj.id])
            )
        return ''

    pause_button.short_description = 'Pause'

    def resume_button(self, obj):
        if not job_status_dict.get(obj.job_name, False):
            return format_html(
                '<a class="button" href="{}">Resume</a>',
                reverse('admin:resume_job', args=[obj.id])
            )
        return ''

    resume_button.short_description = 'Resume'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('start_job/<int:job_id>/', self.start_job, name='start_job'),
            path('pause_job/<int:job_id>/', self.pause_job, name='pause_job'),
            path('resume_job/<int:job_id>/', self.resume_job, name='resume_job'),
        ]
        return custom_urls + urls

    def start_job(self, request, job_id):
        job = ScheduledJob.objects.get(pk=job_id)
        if not job_status_dict.get(job.job_name, False):
            start(job.job_name)
            job_status_dict[job.job_name] = True
            self.message_user(request, f'Started job "{job.job_name}" successfully.')
        else:
            self.message_user(request, f'Job "{job.job_name}" is already running.')
        return redirect('admin:cronjob_scheduledjob_changelist')

    def pause_job(self, request, job_id):
        job = ScheduledJob.objects.get(pk=job_id)
        if job_status_dict.get(job.job_name, False):
            pause(job.job_name)
            job_status_dict[job.job_name] = False
            self.message_user(request, f'Paused job "{job.job_name}" successfully.')
        else:
            self.message_user(request, f'Job "{job.job_name}" is not running.')
        return redirect('admin:cronjob_scheduledjob_changelist')

    def resume_job(self, request, job_id):
        job = ScheduledJob.objects.get(pk=job_id)
        if not job_status_dict.get(job.job_name, False):
            resume(job.job_name)
            job_status_dict[job.job_name] = True
            self.message_user(request, f'Resumed job "{job.job_name}" successfully.')
        else:
            self.message_user(request, f'Job "{job.job_name}" is already running.')
        return redirect('admin:cronjob_scheduledjob_changelist')

@admin.register(JobExecutionLog)
class JobExecutionLogAdmin(admin.ModelAdmin):
    list_display = ('job_name', 'start_time', 'finish_time')
