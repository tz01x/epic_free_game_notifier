from django.db.models import TextChoices

class JobStatusEnum(TextChoices):
    PLANED = 'PLANED','PLANED'
    ACTIVE = 'ACTIVE','ACTIVE'
    FINISHED = 'FINISHED','FINISHED'
    ERROR = 'ERROR','ERROR'