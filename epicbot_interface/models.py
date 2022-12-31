import uuid
from django.db import models
from .enums import JobStatusEnum


class Subscribers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, max_length=32)
    email = models.EmailField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class JobLogs(models.Model):
    job_id = models.CharField(max_length=100)
    status = models.CharField(
        max_length=10,
        choices=JobStatusEnum.choices,
        default=JobStatusEnum.PLANED
    )
    logs = models.TextField(null=True,blank=True)
    next_run_time = models.DateTimeField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.job_id+"  "+ self.status+"  " + str(self.created_at)