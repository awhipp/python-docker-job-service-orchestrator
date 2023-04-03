'''
Job API
'''
from __future__ import annotations

import re
from uuid import uuid4
from fastapi import FastAPI, Request
from services.docker_service import DockerService
from services.scheduler_service import AsyncScheduler

docker_service = DockerService()
scheduler: AsyncScheduler = AsyncScheduler()
bp = FastAPI()

@bp.post('/run')
async def run_job(request: Request):
    '''
    Runs a short-lived job from a container image
    '''
    request = await request.json()
    job_name = " ".join(request['job_name'].strip().split())
    job_name = re.sub(r'[^a-zA-Z0-9]', '_', job_name)
    job_name = f"{job_name}-{str(uuid4())[:8]}"
    image = request['image'].strip() # Image Name or Image ID

    return docker_service.add_job(job_name, image)

@bp.post('/remove')
async def remove_job(request: Request):
    '''
    Removes a short-lived job/container based on container_id
    '''
    request = await request.json()
    job_name = request['job_name']

    return docker_service.remove_job(job_name)

# Get job logs
@bp.post('/logs')
async def get_job_logs(request: Request):
    '''
    Get logs from a short-lived job/container based on container_id
    '''
    request = await request.json()
    job_name = request['job_name']
    return docker_service.get_job_logs(job_name)
