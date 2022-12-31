from django.contrib import admin
from .models import Subscribers,JobLogs


@admin.register(JobLogs)
class JobLogsAdminModel(admin.ModelAdmin):
    list_filter=['status','created_at','next_run_time']
    list_display = ['job_id','status','created_at','next_run_time']

@admin.register(Subscribers)
class SubscribersAdminModel(admin.ModelAdmin):
    search_fields=['email',]
    list_filter=['created_at']
    list_display = ['id','email','created_at','is_active']