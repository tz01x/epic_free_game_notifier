from pytz import utc
from apscheduler.job import Job
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import (
    JobSubmissionEvent,
    JobExecutionEvent,
    EVENT_JOB_SUBMITTED,
    EVENT_JOB_EXECUTED,
    EVENT_JOB_ERROR,
    EVENT_JOB_ADDED
)

from .epic_bot.fetch_promotionalOffers_games import fetch_promo_game
from .models import JobLogs,JobStatusEnum


def on_job_planed(event:JobSubmissionEvent):
    Schedular.initialize()
    job:Job = Schedular.scheduler.get_job(event.job_id)

    if not job:
        return
    
    JobLogs.objects.create(
        job_id=event.job_id,
        status=JobStatusEnum.PLANED,
        next_run_time=job.next_run_time
    )
    
    
def on_job_started(event:JobSubmissionEvent):
    JobLogs.objects.create(
        job_id=event.job_id,
        status=JobStatusEnum.ACTIVE
    )
    
   
def on_job_executed(event:JobExecutionEvent):
    
    Schedular.initialize()
    job:Job = Schedular.scheduler.get_job(event.job_id)

    if not job:
        return

    JobLogs.objects.create(
        job_id=event.job_id,
        status=JobStatusEnum.FINISHED,
        next_run_time=job.next_run_time
    )

def on_job_error(event:JobExecutionEvent):
    
    Schedular.initialize()
    job:Job = Schedular.scheduler.get_job(event.job_id)

    if not job:
        return

    JobLogs.objects.create(
        job_id=event.job_id,
        status=JobStatusEnum.ERROR,
        next_run_time=job.next_run_time,
        logs=str(event.traceback)
    )

class Schedular:
    scheduler = None

    @classmethod
    def initialize(cls):
        if not cls.scheduler:
            cls.scheduler = BackgroundScheduler()
    @classmethod
    def start(cls):
        cls.initialize()
        
        cls.scheduler.add_listener(on_job_planed,EVENT_JOB_ADDED)
        cls.scheduler.add_listener(on_job_started,EVENT_JOB_SUBMITTED)
        cls.scheduler.add_listener(on_job_executed,EVENT_JOB_EXECUTED)
        cls.scheduler.add_listener(on_job_error,EVENT_JOB_ERROR)
        
        cls.scheduler.add_job(
            func=fetch_promo_game,
            trigger='interval',
            minutes=20,
            id='job_fetch_promo_game'
        )

        cls.scheduler.start()
