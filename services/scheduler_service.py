'''
Scheduling service that manages a list of scheduled tasks and executes them.

The scheduled tasks have a cron-like syntax and are tied to a specific job name to run when the schedule is triggered.
'''
from __future__ import annotations

import requests
from apscheduler.job import Job
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore


from services.docker_service import DockerService


class Scheduler():
    '''
    Singleton class for scheduler service
    '''
    __instance: Scheduler = None
    scheduled_tasks: list = None
    docker_service: DockerService = None
    scheduler: AsyncIOScheduler = None

    @staticmethod
    def getInstance() -> Scheduler:
        """ Static access method. """
        if Scheduler.__instance is None:
            Scheduler()
        return Scheduler.__instance
    
    def __init__(self):
        """ Virtually private constructor. """
        if Scheduler.__instance is not None:
            raise ValueError("This class is a singleton!")
        else:
            Scheduler.__instance = self
            self.scheduled_tasks = []
            self.docker_service = DockerService.getInstance()
            job_store = (
                MemoryJobStore()
            )  # FIXME due to a bug in the apscheduler + gunicorn combination
            self.scheduler: AsyncIOScheduler = AsyncIOScheduler(
                jobstores={
                    "default": job_store,
                },
                executors={"default": AsyncIOExecutor(), "cron": ThreadPoolExecutor()},
                # timezone=utc,
                job_defaults={
                    "coalesce": True,  # Trigger only one job to make up for missed jobs.
                    "max_instances": 1,  # Allow only one execution of a job per time.
                },
            )
            self.scheduler.start()
            print('Started Scheduler')

    def schedule_task(self, function, args) -> Job:
        ''' Use apscheduler to schedule a  AsyncIOScheduler task based on a function, args, and a cron string '''
        print("scheduling task")
        # Create args mapping
        print('args', args, 'function', function)
        # Schedule a get request every second
        job = self.scheduler.add_job(
            print,
            args=[
                "http://127.0.0.1:5000/",
            ],
            trigger="cron",
            second="*/1",
        )
        self.scheduled_tasks.append(job)
        print(self.scheduler.get_jobs())
        return job