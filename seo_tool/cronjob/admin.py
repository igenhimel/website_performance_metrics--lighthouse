from django.contrib import admin
from .models import JobExecutionLog,PageScore,ScheduledJob

class JobExecutionLogAdmin(admin.ModelAdmin):
    list_display = ('start_message','job_name', 'start_time','finish_time' )
    list_filter = ('job_name', 'start_time')
    search_fields = ('job_name', 'start_message')

class PageScores(admin.ModelAdmin):
    list_display = ('timestamp','performance_score','seo_score', 'best_practice_score','accessibility_score' )


# Register your model and admin class
admin.site.register(JobExecutionLog, JobExecutionLogAdmin)
admin.site.register(PageScore,PageScores)
admin.site.register(ScheduledJob)
# Register your models here.