from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from .models import ScheduledJob, JobExecutionLog
from django.urls import reverse
from seo_tool.operator import start, pause, resume

# Create a global dictionary to track job statuses
job_status_dict = {}


@admin.register(ScheduledJob)
class ScheduledJobAdmin(admin.ModelAdmin):
    list_display = ('job_name', 'interval',
                    'status_display', 'action_button')

    def status_display(self, obj):
        if job_status_dict.get(obj.job_name, False):
            if job_status_dict[obj.job_name]['paused']:
                # Job is paused, show resume button
                return format_html('<span style="color:red;">&#10007;</span>')
            else:
                # Job is running, show pause button
                return format_html('<span style="color:green;">&#10003;</span>')
        else:
            # Job is not running, show start button
            return format_html('<span style="color:red;">&#10007;</span>')

    status_display.short_description = 'Status'

    def start_selected_jobs(self, request, queryset):
        started_jobs = 0
        for job in queryset:
            if not job_status_dict.get(job.job_name, False):
                start(job.job_name)
                job_status_dict[job.job_name] = True
                started_jobs += 1
        if started_jobs > 0:
            self.message_user(
                request, f'Started {started_jobs} jobs successfully.')

    start_selected_jobs.short_description = 'Start Selected Jobs'

    def pause_selected_jobs(self, request, queryset):
        paused_jobs = 0
        for job in queryset:
            if job_status_dict.get(job.job_name, False):
                pause(job.job_name)
                job_status_dict[job.job_name] = False
                paused_jobs += 1
        if paused_jobs > 0:
            self.message_user(
                request, f'Paused {paused_jobs} jobs successfully.')

    pause_selected_jobs.short_description = 'Pause Selected Jobs'

    def resume_selected_jobs(self, request, queryset):
        resumed_jobs = 0
        for job in queryset:
            if not job_status_dict.get(job.job_name, False):
                resume(job.job_name)
                job_status_dict[job.job_name] = True
                resumed_jobs += 1
        if resumed_jobs > 0:
            self.message_user(
                request, f'Resumed {resumed_jobs} jobs successfully.')

    resume_selected_jobs.short_description = 'Resume Selected Jobs'

    def action_button(self, obj):
        if job_status_dict.get(obj.job_name, False):
            if job_status_dict[obj.job_name]['paused']:
                # Job is paused, show resume button
                return format_html(
                    '<a class="button" href="{}">Resume</a>',
                    reverse('admin:resume_job', args=[obj.id])
                )
            else:
                # Job is running, show pause button
                return format_html(
                    '<a class="button" href="{}">Pause</a>',
                    reverse('admin:pause_job', args=[obj.id])
                )
        else:
            # Job is not running, show start button
            return format_html(
                '<a class="button" href="{}">Start</a>',
                reverse('admin:start_job', args=[obj.id])
            )

    action_button.short_description = 'Action'

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
        if job.job_name not in job_status_dict:
            start(job.job_name)
            job_status_dict[job.job_name] = {'paused': False}
            self.message_user(
                request, f'Started job "{job.job_name}" successfully.')
        else:
            # Toggle: If the job is running, clicking "Start" will pause it.
            pause(job.job_name)
            job_status_dict[job.job_name]['paused'] = True
            self.message_user(
                request, f'Paused job "{job.job_name}" successfully.')
        return redirect('admin:cronjob_scheduledjob_changelist')

    def pause_job(self, request, job_id):
        job = ScheduledJob.objects.get(pk=job_id)
        if job_status_dict.get(job.job_name, False):
            if job_status_dict[job.job_name]['paused']:
                # Toggle: If the job is paused, clicking "Pause" will resume it.
                resume(job.job_name)
                job_status_dict[job.job_name]['paused'] = False
                self.message_user(
                    request, f'Resumed job "{job.job_name}" successfullysss.')
            else:
                # Toggle: If the job is running, clicking "Pause" will pause it.
                pause(job.job_name)
                job_status_dict[job.job_name]['paused'] = True
                self.message_user(
                    request, f'Paused job "{job.job_name}" successfully.')
        return redirect('admin:cronjob_scheduledjob_changelist')

    def resume_job(self, request, job_id):
        job = ScheduledJob.objects.get(pk=job_id)
        if job_status_dict.get(job.job_name, False):
            if job_status_dict[job.job_name]['paused']:
                # Toggle: Clicking "Resume" will resume the paused job.
                resume(job.job_name)
                job_status_dict[job.job_name]['paused'] = False
                self.message_user(
                    request, f'Resumed job "{job.job_name}" successfullys.')
            else:
                # Toggle: Clicking "Resume" will pause the job.
                pause(job.job_name)
                job_status_dict[job.job_name]['paused'] = True
                self.message_user(
                    request, f'Paused job "{job.job_name}" successfully.')
        return redirect('admin:cronjob_scheduledjob_changelist')


@admin.register(JobExecutionLog)
class JobExecutionLogAdmin(admin.ModelAdmin):
    list_display = ('job_name','message','start_time', 'finish_time')
