'''
Service API
'''
from __future__ import annotations

import re
from uuid import uuid4
from fastapi import FastAPI, Request
from services.docker_service import DockerService

client = DockerService().client
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

    print(f"Adding service: [{service_name}] from image: [{image}]")

    # create service
    service = client.services.create(image, name=service_name)
    return {'message': 'Service created successfully', 'service_name': service.name}


@bp.put('/scale')
async def scale_service(request: Request):
    '''
    Scales a long-running service based on service_id
    '''
    request = await request.json()
    service_name = request['service_name']
    replicas = int(request['replicas'])
    service = client.services.list(filters={'name': service_name})[0]
    service.scale(replicas=replicas)
    return {'message': 'Service scaled successfully', 'service_name': service_name, 'replicas': replicas}

@bp.post('/remove')
async def remove_service(request: Request):
    '''
    Removes a long-running service based on service name
    '''
    request = await request.json()
    service_name = request['service_name']
    service = client.services.list(filters={'name': service_name})[0]
    service.remove()
    return {'message': 'Service removed successfully', 'service_name': service_name}

# TODO: Use since, until to paginate since last request and append
@bp.post('/logs')
async def get_service_logs(request: Request):
    '''
    Get logs from a long-running service based on service name
    '''
    request = await request.json()
    service_name = request['service_name']
    service = client.services.list(filters={'name': service_name})[0]
    log_generator = service.logs(since=0, stdout=True, stderr=True)
    logs = ''.join([log.decode('utf-8') for log in log_generator])
    return {'message': 'Service logs retrieved successfully', 'service_name': service_name, 'logs': logs}