from django.contrib import admin
from .models import JobExecutionLog,PageScore

class JobExecutionLogAdmin(admin.ModelAdmin):
    list_display = ('start_message','job_name', 'start_time','finish_time' )
    list_filter = ('job_name', 'start_time')
    search_fields = ('job_name', 'start_message')

# Register your model and admin class
admin.site.register(JobExecutionLog, JobExecutionLogAdmin)
admin.site.register(PageScore)
# Register your models here.
