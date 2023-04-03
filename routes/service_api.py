'''
Service API
'''
from __future__ import annotations

import re
from uuid import uuid4
from fastapi import FastAPI, Request
from services.docker_service import DockerService

docker_service = DockerService()
bp = FastAPI()


@bp.post('/add')
async def add_service(request: Request):
    '''
    Adds a long-running service from a container image
    '''
    request = await request.json()
    service_name = " ".join(request['service_name'].strip().split())
    service_name = re.sub(r'[^a-zA-Z0-9]', '_', service_name)
    service_name = f"{service_name}-{str(uuid4())[:8]}"
    image = request['image'].strip() # Image Name or Image ID

    return docker_service.add_service(service_name, image)


@bp.put('/scale')
async def scale_service(request: Request):
    '''
    Scales a long-running service based on service_id
    '''
    request = await request.json()
    service_name = request['service_name']
    replicas = int(request['replicas'])
    return docker_service.scale_service(service_name, replicas)

@bp.post('/remove')
async def remove_service(request: Request):
    '''
    Removes a long-running service based on service name
    '''
    request = await request.json()
    service_name = request['service_name']
    return docker_service.remove_service(service_name)

# TODO: Use since, until to paginate since last request and append
@bp.post('/logs')
async def get_service_logs(request: Request):
    '''
    Get logs from a long-running service based on service name
    '''
    request = await request.json()
    service_name = request['service_name']
    return docker_service.get_service_logs(service_name)