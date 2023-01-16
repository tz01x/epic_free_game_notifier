from django.contrib import admin
from .models import Subscribers,JobLogs
from epicbot_interface.epic_bot.fetch_promotionalOffers_games import fetch_promo_game

@admin.action(description='Fetch New Data and Notify All')
def fetch_new_data_action(modeladmin, request, queryset):
    fetch_promo_game()
    

@admin.register(JobLogs)
class JobLogsAdminModel(admin.ModelAdmin):
    list_filter=['status','created_at','next_run_time']
    list_display = ['job_id','status','created_at','next_run_time']

@admin.register(Subscribers)
class SubscribersAdminModel(admin.ModelAdmin):
    search_fields=['email',]
    list_filter=['created_at']
    list_display = ['id','email','created_at','is_active']
    actions = [fetch_new_data_action]