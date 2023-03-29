'''
Job API
'''
from __future__ import annotations

import re
from uuid import uuid4
from fastapi import FastAPI, Request
from services.docker_service import DockerService
from services.scheduler_service import AsyncScheduler

client = DockerService().client
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

    print(
        f"Running job: [{job_name}] from image: [{image}]"
    )

    client.containers.run(image, detach=True, name=job_name)
    return {'message': 'Job started successfully', 'job_name': job_name}

@bp.post('/remove')
async def remove_job(request: Request):
    '''
    Removes a short-lived job/container based on container_id
    '''
    request = await request.json()
    job_name = request['job_name']
    container = client.containers.get(job_name)
    container.stop()
    container.remove(force=True)
    return {'message': 'Job removed successfully', 'job_name': job_name}

# Get job logs
# TODO: Use since, until to paginate since last request and append
@bp.post('/logs')
async def get_job_logs(request: Request):
    '''
    Get logs from a short-lived job/container based on container_id
    '''
    request = await request.json()
    job_name = request['job_name']
    container = client.containers.get(job_name)
    logs = container.logs(tail='all', stdout=True, stderr=True)
    logs = logs.decode('utf-8')
    return {'message': 'Job logs retrieved successfully', 'job_name': job_name, 'logs': logs}
