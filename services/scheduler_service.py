'''
Scheduling service that manages a list of scheduled tasks and executes them.

The scheduled tasks have a cron-like syntax and are tied to a specific job name to run when the schedule is triggered.
'''
from __future__ import annotations

import time
import asyncio
import datetime
from typing import Callable
from croniter import croniter

from services.docker_service import DockerService


async def recurring_wrapper(scheduler: AsyncScheduler, task_name, cron_string: str, function: Callable, *args, **kwargs):
    '''
    Wrapper function for recurring tasks.
    '''
    try:
        while True:
            next_run_time = croniter(cron_string, scheduler.loop.time()).get_next()
            sleep_time = round(max(next_run_time - scheduler.loop.time(), 0), 2)
            await asyncio.sleep(sleep_time)
            function(*args, **kwargs)
    except Exception as job_exception: # pylint: disable=broad-except
        # TODO - Handle job exceptions
        print(f"[{time.ctime()}] Error in task {task_name}: {job_exception}")

async def scheduled_wrapper(task_name, dtime_string: datetime, function: Callable, *args, **kwargs):
    '''
    Wrapper function for scheduled tasks.
    '''
    try:
        if isinstance(dtime_string, str):
            dtime = datetime.datetime.strptime(dtime_string, "%Y-%m-%d %H:%M:%S")
        else:
            dtime = dtime_string

        await asyncio.sleep(dtime.timestamp() - time.time())
        await function(*args, **kwargs)
    except Exception as job_exception: # pylint: disable=broad-except
        # TODO - Handle job exceptions
        print(f"[{time.ctime()}] Error in task {task_name}: {job_exception}")

class AsyncScheduler:
    __instance = None
    loop = None
    tasks = None
    docker_service: DockerService = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.tasks = []
        self.docker_service = DockerService().client

    def schedule_task(self, task_name: str, recurring: bool, dtime_string: str, function: Callable, *args, **kwargs):
        '''
        Schedules a task to run at a specific time.

        Args:
            task_name (str): Name of the task to run
            recurring (bool): Whether the task should be run repeatedly
            dtime_string (str): Cron-like string or datetime to schedule the task
            function (Callable): Function to run
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function
        '''
        # Make function a coroutine if it isn't already
        # if not asyncio.iscoroutinefunction(function):
        #     function = asyncio.coroutine(function)
        
        if recurring:
            print(f"[{time.ctime()}] Scheduling task {task_name} to run at {dtime_string} (Recurring = {recurring}).")
            self.tasks.append(
                self.loop.create_task(
                    recurring_wrapper(self, task_name, dtime_string, function, *args, **kwargs)
                )
            )
        else:
            print(f"[{time.ctime()}] Scheduling task {task_name} to run at {dtime_string} (Recurring = {recurring}).")
            self.tasks.append(
                self.loop.create_task(
                    scheduled_wrapper(task_name, dtime_string, function, *args, **kwargs)
                )
            )

    async def stop_tasks(self):
        for task in self.tasks:
            task.cancel()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.stop_tasks()
