'''
Image API
'''
from __future__ import annotations

from fastapi import FastAPI, Request
from services.docker_service import DockerService

docker_service = DockerService()
bp = FastAPI()

@bp.post('/add')
async def add_image(request: Request):
    '''
    Add a container image to the local docker registry
    '''
    request = await request.json()
    image_name = " ".join(request['image_name'].strip().split())
    image_version = " ".join(request['image_version'].strip().split())
    return docker_service.add_image(image_name, image_version)

@bp.post('/remove')
async def remove_image(request: Request):
    '''
    Add a container image to the local docker registry
    '''
    request = await request.json()
    image_name = " ".join(request['image_name'].strip().split())
    return docker_service.remove_image(image_name)
